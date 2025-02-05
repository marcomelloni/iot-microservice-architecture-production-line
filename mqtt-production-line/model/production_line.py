import paho.mqtt.client as mqtt

from typing import Dict
from .robot_arm import RobotArm
import json
import time


class ProductionLine:
    """
    Represents a production line with multiple robot arms.
    Manages the activation, deactivation, and monitoring of the robot arms.
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
        """
        Deactivates the production line and stops the robot arms.
        Also stops the monitoring and publishing process.
        """
        self.active = False
        self.monitoring_active = False
        for robot_arm in self.robot_arms.values():
            robot_arm.stop()
            robot_arm.reset()
        print(f"Production line {self.line_id} deactivated.")

    def activate(self):
        """Activates the production line and starts the robot arms"""
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
            print(f"Published: {topic} with data {sensor_data}")
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
        """Inizializza e avvia il client MQTT con sottoscrizione ai comandi"""
        self.mqtt_client = mqtt.Client(f"production-line-{self.line_id}")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message  # Aggiungi gestione messaggi
        self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)
        
        self.mqtt_client.subscribe(f"{MQTT_BASIC_TOPIC}/command")  # Ascolta i comandi
        self.mqtt_client.loop_start()


    def stop_mqtt_client(self):
        """Stops the MQTT client"""
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            print("MQTT client disconnected.")

    def monitor_and_publish(self):
        """
        Simulates monitoring sensors and publishes the data to the appropriate MQTT topics.
        Runs in a loop while the production line is active.
        """
        self.monitoring_active = True  # Enable monitoring
        while self.active == True and self.monitoring_active:

            for robot_arm in self.robot_arms.values():
                payload_joint_consumptions = robot_arm.get_json_consumptions()
                payload_grip = robot_arm.get_json_grip()

                topic_joints_consumption = f"{MQTT_BASIC_TOPIC}/{robot_arm.arm_id}/telemetry/joints_consumption"
                topic_grip = f"{MQTT_BASIC_TOPIC}/{robot_arm.arm_id}/telemetry/grip"

                self.publish_measurement(payload_joint_consumptions, topic_joints_consumption)
                self.publish_measurement(payload_grip, topic_grip)
            time.sleep(3)

    def stop_monitor_and_publish(self):
        """Stops the monitoring and publishing process"""
        self.monitoring_active = False  # Disables the monitoring loop
        print("Stopped monitoring and publishing.")

