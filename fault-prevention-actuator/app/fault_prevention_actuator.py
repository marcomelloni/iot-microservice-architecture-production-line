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


robot_consumption_data = {}
total_consumption_all_robots = 0  # Variable to store total consumption of all robots


def on_message(client, userdata, msg):
    """
    Callback function for when a PUBLISH message is received from the server.

    :param client: The client instance for this callback.
    :param userdata: The private user data as set in Client() or userdata_set().
    :param msg: An instance of MQTTMessage, which contains topic, payload, qos, retain.
    """
    if mqtt.topic_matches_sub(mqtt_topic, msg.topic):  # Check the MQTT topic
        try:
            # Decode the incoming MQTT message
            payload = json.loads(msg.payload.decode())
            robot_id = msg.topic.split('/')[1]
            message = msg.topic.split('/')[3]

            if message == "joints_consumption":
                # Extract joint consumption data from the payload
                if payload.get('joint_consumption_sensors'):
                    # Loop through the joint consumption sensors data
                    for sensor in payload['joint_consumption_sensors']:
                        # Extract joint_id and its consumption
                        joint_id = sensor.get('joint_id', 'N/A')
                        current_sensor = sensor.get('current_sensor', {})
                        consumption = current_sensor.get('value', 0.0)  # Get the current consumption value

                        if consumption > 100:
                            # If consumption exceeds 100, send a stop signal to the production line
                            mqtt_topic_publish = "production_line/control/stop"
                            value = True
                            client.publish(mqtt_topic_publish, json.dumps(value), qos=2)
                            print(
                                f"Published message to {mqtt_topic_publish} with payload {value} because {joint_id} consumed {consumption} A")

                            # Get the current time for fault logging
                            timenow = datetime.now()

                            # Prepare the POST request payload
                            target_url = f"{api_url}/faults"
                            payload_desired = {
                                "robot_id": payload.get('robot_arm_id', 'N/A'),
                                "fault": f"Robot {payload.get('robot_arm_id', 'N/A')} - Joint {joint_id} consumed {consumption} A at {timenow}"
                            }

                            # Send the fault report via POST request
                            response = requests.post(target_url, json=payload_desired)
                            print(
                                f"POST request to {target_url} with payload {payload_desired} returned {response.status_code}")

                            return

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
