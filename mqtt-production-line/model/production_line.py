import paho.mqtt.client as mqtt
from typing import Dict
from model.robot_arm import RobotArm
import json
import time

BROKER_ADDRESS = "0.0.0.0"  # Address of the MQTT broker
BROKER_PORT = 1883  # Port of the broker (using the standard port)
MQTT_USERNAME = "iot-project-Melloni-Angelini-Morselli"  
MQTT_PASSWORD = "password"  
MQTT_BASIC_TOPIC = f"robot"  # Base topic

class ProductionLine:
    def __init__(self, line_id: str):
        self.line_id: str = line_id
        self.robot_arms: Dict[str, RobotArm] = {}  # Dictionary of robot arms
        self.active: bool = True  # Active state of the production line
        self.mqtt_client: mqtt.Client = None  # MQTT client
        self.mqtt_connected: bool = False  # MQTT connection status

    def add_robot_arm(self, robot_arm: RobotArm):
        """Adds a robot arm to the production line"""
        self.robot_arms[robot_arm.arm_id] = robot_arm

    def deactivate(self):
        """Deactivates the production line and stops the robot arms"""
        self.active = False
        for robot_arm in self.robot_arms.values():
            robot_arm.stop()
            robot_arm.reset()
        self.stop_monitor_and_publish()
        print(f"Production line {self.line_id} deactivated.")

    def activate(self):
        """Activates the production line"""
        self.active = True
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

    def start_mqtt_client(self):
        """Initializes and starts the MQTT client"""
        self.mqtt_client = mqtt.Client(f"production-line-{self.line_id}")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)
        self.mqtt_client.loop_start()  # Starts the loop for the MQTT connection

    def stop_mqtt_client(self):
        """Stops the MQTT client"""
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            print("MQTT client disconnected.")

    def monitor_and_publish(self):
        """Simulate monitoring sensors and publish the data to the appropriate MQTT topics"""
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