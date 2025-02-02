import json
import paho.mqtt.client as mqtt
import yaml
import requests
from datetime import datetime


# Default Values
CONF_FILE_PATH = "actuator_conf.yaml"

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

robot_consumption_data = {}
total_consumption_all_robots = 0  # Variable to store total consumption of all robots

def on_message(client, userdata, msg):
    if mqtt.topic_matches_sub(mqtt_topic, msg.topic):  # Check the MQTT topic
        try:
            # Decode the incoming MQTT message
            payload = json.loads(msg.payload.decode())
            robot_id = msg.topic.split('/')[1]
            message = msg.topic.split('/')[3]

            if message == "joints_consumption":
                # Extract joint consumption data from the payload
                for sensor in payload.get('joint_consumption_sensors', []):
                    for joint in sensor.get('joints', []):
                        consumption = joint.get('consumption', 0)
                        joint_id = joint.get('joint_id', 'N/A')
                        if consumption > 100:
                            # If consumption exceeds 100, send a stop signal
                            mqtt_topic_publish = "production_line/control/stop"
                            value = True
                            client.publish(mqtt_topic_publish, json.dumps(value), qos=2)
                            print(f"Published message to {mqtt_topic_publish} with payload {value} because {robot_id} - {joint_id} consumed {consumption} kW")
                            
                            
                            timenow = datetime.now()
                            target_url = f"{api_url}/faults"
                            payload_desired = {
                                "robot_id": robot_id,
                                "fault": f"Robot {robot_id} - Joint {joint_id} consumed {consumption} kW at {timenow}"
                            }

                            response = requests.post(target_url, json=payload_desired)
                            print(f"POST request to {target_url} with payload {payload} returned {response.status_code}")
                            return  # Stop after publishing once

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
      