import json
import requests
import paho.mqtt.client as mqtt
import yaml
import time

# Default Values
CONF_FILE_PATH = "fetcher_conf.yaml"

# Default Configuration Dictionary
configuration_dict = {
    "broker_ip": "127.0.0.1",
    "broker_port": 1883,
    "target_telemetry_topic": "robot/+/telemetry/#",
    "device_api_url": "http://127.0.0.1:7070/api/v1/productionline/robot"
}

# Read Configuration from target Configuration File Path
def read_configuration_file():
    global configuration_dict

    with open(CONF_FILE_PATH, 'r') as file:
        configuration_dict = yaml.safe_load(file)

    return configuration_dict

configuration_dict = read_configuration_file()

print("Read Configuration from file ({}): {}".format(CONF_FILE_PATH, configuration_dict))

# MQTT Broker Configuration
mqtt_broker_host = configuration_dict["broker_ip"]
mqtt_broker_port = configuration_dict["broker_port"]
mqtt_topic = configuration_dict["target_telemetry_topic"]

# HTTP API Configuration
api_url = configuration_dict["device_api_url"]

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):

    if mqtt.topic_matches_sub(mqtt_topic, msg.topic):
        try:
            payload = json.loads(msg.payload.decode())
            robot_id = msg.topic.split('/')[1]
            message = msg.topic.split('/')[3]
            print(f'{robot_id} - {message} - {payload}')
            
            if message == "joints_consumption":
                target_url = f"{api_url}/{robot_id}/telemetry/joints_consumption"
                """
                    payload_incoming = {'robot_arm_id': 'RA_002', 'joint_consumption_sensors': [
                    {'joint_id': 'joint_0', 'current_sensor': {'device_id': 'joint_0', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 0.0, 'unit': 'A', 'timestamp': '2025-02-05T09:32:40.788389'}},
                    {'joint_id': 'joint_1', 'current_sensor': {'device_id': 'joint_1', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 0.0, 'unit': 'A', 'timestamp': '2025-02-05T09:32:40.788394'}},
                    {'joint_id': 'joint_2', 'current_sensor': {'device_id': 'joint_2', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 0.0, 'unit': 'A', 'timestamp': '2025-02-05T09:32:40.788398'}}
                    ]}
                """
                payload_desired = {
                    "joints": [
                        {
                            "joint_id": joint["joint_id"],  
                            "consumption": joint["current_sensor"]["value"],  
                            "timestamp": joint["current_sensor"]["timestamp"]  
                        }
                        for joint in payload['joint_consumption_sensors']
                    ]
                }
                
                response = requests.post(target_url, json=payload_desired)
                print(f"POST request to {target_url} with payload {payload} returned {response.status_code}")
                time.sleep(1)
                
            elif message == "grip":
                target_url = f"{api_url}/{robot_id}/telemetry/weight_ee"
                weight = payload # convert from grip value to weight
                grip_force_newton = payload['grip_sensors'][0]['value']
                gravitational_constant = 9.81  # Acceleration [m/s^2]

                # Conversione da Newton a kg
                weight_kg = grip_force_newton / gravitational_constant

                # Creazione del payload desiderato
                payload_desired = {
                    "weight_ee": round(weight_kg, 2)  # Arrotondato a 2 decimali
                }

                response = requests.post(target_url, json=payload_desired)
                print(f"POST request to {target_url} with payload {weight} returned {response.status_code}")
                time.sleep(1)
                
            else:
                print(f"Unknown message type: {message}")
        except Exception as e:
            print(f"Error processing MQTT message: {str(e)}")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(mqtt_broker_host, mqtt_broker_port, 60)

# Start the MQTT loop
client.loop_forever()



