import paho.mqtt.client as mqtt
import time
from typing import Dict
from model.robot_arm import RobotArm
# from model.current_sensor import CurrentSensor
# from model.grip_sensor import GripSensor

BROKER_ADDRESS = "0.0.0.0"  # Indirizzo del broker MQTT
BROKER_PORT = 1883  # Porta del broker (usiamo la porta standard)
MQTT_USERNAME = "iot-project-Melloni-Angelini-Morselli"  # Sostituisci con il tuo username
MQTT_PASSWORD = "password"  # Sostituisci con la tua password
MQTT_BASIC_TOPIC = f"robot"  # Topic base

class ProductionLine:
    def __init__(self, line_id: str):
        self.line_id: str = line_id
        self.robot_arms: Dict[str, RobotArm] = {}  # Dizionario di bracci robotici
        self.active: bool = True  # Stato attivo della linea di produzione
        self.mqtt_client: mqtt.Client = None  # Client MQTT
        self.mqtt_connected: bool = False  # Stato connessione MQTT

    def add_robot_arm(self, robot_arm: RobotArm):
        """Aggiungi un braccio robotico alla linea di produzione"""
        self.robot_arms[robot_arm.arm_id] = robot_arm

    def deactivate(self):
        """Disattiva la linea di produzione e ferma i bracci robotici"""
        self.active = False
        for robot_arm in self.robot_arms.values():
            robot_arm.reset()
        print(f"Linea di produzione {self.line_id} disattivata.")

    def activate(self):
        """Attiva la linea di produzione"""
        self.active = True
        print(f"Linea di produzione {self.line_id} attivata.")

    def on_connect(self, client, userdata, flags, rc):
        """Callback quando si stabilisce la connessione MQTT"""
        if rc == 0:
            self.mqtt_connected = True
            print("Connesso al broker MQTT con successo!")
        else:
            print(f"Errore di connessione MQTT: {rc}")

    def publish_measurement(self, sensor_data: Dict, topic: str):
        """Pubblica i dati del sensore sul topic MQTT"""
        if self.mqtt_connected:
            self.mqtt_client.publish(topic, str(sensor_data), qos=0, retain=False)
            print(f"Pubblicato: {topic} con dati {sensor_data}")
        else:
            print("Errore: non connesso al broker MQTT.")

    def start_mqtt_client(self):
        """Inizializza e avvia il client MQTT"""
        self.mqtt_client = mqtt.Client(f"production-line-{self.line_id}")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)
        self.mqtt_client.loop_start()  # Avvia il loop per la connessione MQTT

    def stop_mqtt_client(self):
        """Ferma il client MQTT"""
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            print("Client MQTT disconnesso.")
    
    def monitor_and_publish(self):
        """Simulate monitoring sensors and publish the data to the appropriate MQTT topics"""
        while self.active:
            for robot_arm in self.robot_arms.values():
                
                payload_joint_consumptions = robot_arm.get_json_joint_consumptions()        
                payload_grip = robot_arm.get_json_grip()
                
                topic_joints_consumption = f"{MQTT_BASIC_TOPIC}/{robot_arm.arm_id}/telemetry/joints_consumption"
                topic_grip = f"{MQTT_BASIC_TOPIC}/{robot_arm.arm_id}/telemetry/grip"
                
                self.publish_measurement(payload_joint_consumptions, topic_joints_consumption)
                self.publish_measurement(payload_grip, topic_grip)
                

