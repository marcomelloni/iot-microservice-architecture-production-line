"""
This script acts as an MQTT consumer for the production line control system.
It listens for stop commands on a specific topic and deactivates the production line when a stop command is received.
"""

import paho.mqtt.client as mqtt
import json
import time
from production_line_producer import \
    deactivate_production_line  # Import the production line deactivation function from the producer

# Configuration variables
client_id = "ProductionLine-Consumer"
broker_ip = "127.0.0.1"  # Broker IP address
broker_port = 1883  # Broker port
target_topic_filter = "production_line/control/stop"  # Topic for the stop command

# Create a new MQTT client
mqtt_client = mqtt.Client(client_id)


def on_connect(client, userdata, flags, rc):
    """
    Called when the client connects to the broker.
    Subscribes to the target topic after a successful connection.
    """
    print(f"Connected with result code {rc}")
    mqtt_client.subscribe(target_topic_filter)
    print(f"Subscribed to: {target_topic_filter}")


def on_message(client, userdata, message):
    """
    Called when a message is received.
    Processes the received message and deactivates the production line if the payload is True.
    """
    if mqtt.topic_matches_sub(target_topic_filter, message.topic):
        try:
            message_payload = message.payload.decode("utf-8")
            payload_data = json.loads(message_payload)

            if isinstance(payload_data, bool) and payload_data:
                deactivate_production_line()
                print("Production line stopped.")

            print(f"Message received on topic {message.topic}: {payload_data}")

        except json.JSONDecodeError:
            print("Error decoding JSON payload.")

# Attach the callback methods
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

# Connect to the MQTT broker
mqtt_client.connect(broker_ip, broker_port)

# Start the MQTT client loop (this will block execution and keep the program running)
mqtt_client.loop_start()

# Keep the consumer running to listen for commands
while True:
    time.sleep(1)  # Keep the loop active to listen for messages

