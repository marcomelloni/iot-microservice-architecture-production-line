import paho.mqtt.client as mqtt
from typing import Dict
from model.robot_arm import RobotArm
import json

BROKER_ADDRESS = "0.0.0.0"  # Address of the MQTT broker
BROKER_PORT = 1883  # Port of the broker (using the standard port)
MQTT_USERNAME = "iot-project-Melloni-Angelini-Morselli"
MQTT_PASSWORD = "password"
MQTT_BASIC_TOPIC = f"robot"  # Base topic


class ProductionLine:
    """
    Represents a production line that manages robot arms and communicates with an MQTT broker.
    It can receive commands to start or stop the production line and publish telemetry data.
    """

    def __init__(self, line_id: str):
        self.line_id: str = line_id
        self.robot_arms: Dict[str, RobotArm] = {}
        self.active: bool = True
        self.mqtt_client: mqtt.Client = None
        self.mqtt_connected: bool = False
        self.stopped: bool = False  # Flag to track if STOP was received

    def add_robot_arm(self, robot_arm: RobotArm):
        """Adds a robot arm to the production line"""
        self.robot_arms[robot_arm.arm_id] = robot_arm

    def deactivate(self):
        """Deactivates the production line and stops the robot arms"""
        self.active = False
        self.monitoring_active = False
        for robot_arm in self.robot_arms.values():
            robot_arm.stop()
            robot_arm.reset()
        print(f"Production line {self.line_id} deactivated.")

    def activate(self):
        """Activates the production line"""
        self.active = True
        self.monitoring_active = True
        for robot_arm in self.robot_arms.values():
            robot_arm.start()
        print(f"Production line {self.line_id} activated.")

    def on_connect(self, client, userdata, flags, rc):
        """Callback when the MQTT connection is established"""
        if rc == 0:
            self.mqtt_connected = True
            print("Connected to the MQTT broker successfully!")
        else:
            print(f"MQTT connection error: {rc}")

    def publish_measurement(self, sensor_data: Dict, topic: str):
        """Publishes sensor data to the MQTT topic"""
        if self.mqtt_connected:
            self.mqtt_client.publish(topic, json.dumps(sensor_data), qos=0, retain=False)
            #print(f"Published: {topic} with data {sensor_data}")
        else:
            print("Error: not connected to the MQTT broker.")

    def on_message(self, client, userdata, msg):
        """Handles incoming MQTT messages"""
        payload = msg.payload.decode("utf-8")
        print(f"[DEBUG] Received message on topic {msg.topic}: {payload}")

        if payload == "STOP":
            if self.stopped:  # Skip if already stopped
                print("[DEBUG] STOP command ignored (already stopped)")
                return
            self.deactivate()  # Stop the production line
            self.stop_mqtt_client()  # Stop the MQTT client
            self.stopped = True  # Mark as stopped

        elif payload == "START":
            if not self.stopped:  # Skip if already running
                print("[DEBUG] START command ignored (already running)")
                return
            self.start_mqtt_client()  # Start the MQTT client
            self.activate()  # Restart the production line
            self.stopped = False  # Reset stopped flag

    def start_mqtt_client(self):
        """Initializes and starts the MQTT client with command subscription and Last Will message"""
        self.mqtt_client = mqtt.Client(f"production-line-{self.line_id}")
        
        # Set up the Last Will and Testament (LWT) message
        lwt_topic = f"{MQTT_BASIC_TOPIC}/production-line/status"
        lwt_message = json.dumps({"status": "disconnected", "line_id": self.line_id})
        self.mqtt_client.will_set(lwt_topic, payload=lwt_message, qos=1, retain=False)
        
        # Set callback functions for handling MQTT events
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message  # Add message handling function
        
        # Set MQTT credentials
        self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)
        self.mqtt_client.subscribe(f"{MQTT_BASIC_TOPIC}/command")
        self.mqtt_client.loop_start()
        print(f"MQTT client started for production line {self.line_id}")

    def stop_mqtt_client(self):
        """Stops the MQTT client and sends Last Will message"""
        if self.mqtt_client:
            # Send a "stopped" status message if the client disconnects normally
            lwt_topic = f"{MQTT_BASIC_TOPIC}/production-line/status"
            lwt_message = json.dumps({"status": "stopped", "line_id": self.line_id})
            result = self.mqtt_client.publish(lwt_topic, payload=lwt_message, qos=1, retain=False)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[DEBUG] LWT message sent to topic {lwt_topic} with payload {lwt_message}")
            else:
                print(f"[ERROR] Failed to send LWT message, result code: {result.rc}")

    def monitor_and_publish(self):
        """Simulates monitoring and publishing MQTT data"""
        self.monitoring_active = True
        try:
            while self.active and self.monitoring_active:
                #print(f"[DEBUG] Monitoring active: {self.monitoring_active}, Production line active: {self.active}")
                for robot_arm in self.robot_arms.values():
                    payload_joint_consumptions = robot_arm.get_json_consumptions()
                    payload_grip = robot_arm.get_json_grip()

                    topic_joints_consumption = f"{MQTT_BASIC_TOPIC}/{robot_arm.arm_id}/telemetry/joints_consumption"
                    topic_grip = f"{MQTT_BASIC_TOPIC}/{robot_arm.arm_id}/telemetry/grip"

                    self.publish_measurement(payload_joint_consumptions, topic_joints_consumption)
                    self.publish_measurement(payload_grip, topic_grip)
        except KeyboardInterrupt:
            # Handle graceful exit on user interruption
            print("[DEBUG] Monitoring interrupted by user.")
        except Exception as e:
            # Log unexpected errors
            print(f"[ERROR] An error occurred: {e}")
        finally:
            # Ensure that the MQTT client is stopped, and LWT is sent in any case
            print("[DEBUG] Exiting monitoring loop.")
            self.stop_mqtt_client()  # Ensure LWT message is sent
