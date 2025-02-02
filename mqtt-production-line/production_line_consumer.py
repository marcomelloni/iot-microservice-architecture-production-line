import paho.mqtt.client as mqtt
import json
import time
from production_line_producer import production_line

# Configuration variables
client_id = "ProductionLine-Consumer"
broker_ip = "127.0.0.1"  # Broker IP address
broker_port = 1883  # Broker port
target_topic_filter = "production_line/control/stop"  # Topic to listen for the stop command


# Create a new MQTT Client
mqtt_client = mqtt.Client(client_id)

# Define the callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    """Called when the client connects to the broker."""
    print(f"Connected with result code {rc}")
    # Subscribe to the topic after successful connection
    mqtt_client.subscribe(target_topic_filter)
    print(f"Subscribed to: {target_topic_filter}")

# Define a callback to handle received messages
def on_message(client, userdata, message):
    """Called when a message is received."""
    
    # Check if the received message matches the topic filter
    if mqtt.topic_matches_sub(target_topic_filter, message.topic):
        try:
            # Decode the message payload as a string
            message_payload = message.payload.decode("utf-8")
            payload_data = json.loads(message_payload)  # Assume the payload is JSON-encoded

            # If payload_data is a boolean, directly use it.
            if isinstance(payload_data, bool):  
                if payload_data:  # Check if it's True
                    production_line.deactivate()
                    time.sleep(5)
                    print("Production line deactivated.")
            
            print(f"Received message on topic {message.topic}: {payload_data}")

        except json.JSONDecodeError:
            print("Error decoding JSON payload.")


# Attach the callback methods
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

# Connect to the MQTT Broker
mqtt_client.connect(broker_ip, broker_port)

# Start the MQTT client loop (this will block and keep the program running)
mqtt_client.loop_forever()