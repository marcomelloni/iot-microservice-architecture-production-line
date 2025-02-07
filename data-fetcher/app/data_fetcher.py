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
    "device_api_url": "http://127.0.0.1:7070/api/v1/productionline/robot",
    "target_lwt_topic": "robot/production-line/status"
}


def read_configuration_file():
    """
    Reads the configuration from the specified YAML file and updates the global configuration dictionary.

    :return: The updated configuration dictionary.
    """
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
    """
    Callback function for when the client receives a CONNACK response from the server.

    :param client: The client instance for this callback.
    :param userdata: The private user data as set in Client() or userdata_set().
    :param flags: Response flags sent by the broker.
    :param rc: The connection result.
    """
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(mqtt_topic)


def on_message(client, userdata, msg):
    """
    Callback function for when a PUBLISH message is received from the server.

    :param client: The client instance for this callback.
    :param userdata: The private user data as set in Client() or userdata_set().
    :param msg: An instance of MQTTMessage, which contains topic, payload, qos, retain.
    """
        
    if mqtt.topic_matches_sub(mqtt_topic, msg.topic):
        try:
            payload = json.loads(msg.payload.decode())
            robot_id = msg.topic.split('/')[1]
            message = msg.topic.split('/')[3]
            #print(f'{robot_id} - {message} - {payload}')

            if message == "joints_consumption":
                target_url = f"{api_url}/{robot_id}/telemetry/joints_consumption"
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
                #time.sleep(1)

            elif message == "grip":
                target_url = f"{api_url}/{robot_id}/telemetry/weight_ee"
                grip_force_newton = payload['grip_sensors'][0]['value']
                gravitational_constant = 9.81  # Acceleration [m/s^2]

                # Conversion from Newton to kg
                weight_kg = grip_force_newton / gravitational_constant

                # Create the desired payload
                payload_desired = {
                    "weight_ee": round(weight_kg, 2)  # Rounded to 2 decimal places
                }

                response = requests.post(target_url, json=payload_desired)
                print(f"POST request to {target_url} with payload {weight_kg} returned {response.status_code}")
                #time.sleep(1)

            else:
                print(f"Unknown message type: {message}")
        except Exception as e:
            print(f"Error processing MQTT message: {str(e)}")
            
    if msg.topic == "robot/production-line/status":
        print(f"Production Line Status: {msg.payload.decode()}")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(mqtt_broker_host, mqtt_broker_port, 60)

# Start the MQTT loop
client.loop_forever()
