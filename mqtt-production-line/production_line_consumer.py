import paho.mqtt.client as mqtt
import json
import time
from production_line_producer import production_line  # Import without starting production

# MQTT Configuration
client_id = "actuator-consumer"
broker_ip = "127.0.0.1"  
broker_port = 1883  
target_topic_filter = "production_line/control/stop"  
MQTT_LINE_BASIC_TOPIC = "robot"

# Create MQTT client
mqtt_client = mqtt.Client(client_id)

def on_connect(client, userdata, flags, rc):
    """Callback when connected to the broker"""
    print(f"Connected with result code {rc}")
    mqtt_client.subscribe(target_topic_filter)
    print(f"Subscribed to topic: {target_topic_filter}")

def on_message(client, userdata, message):
    """Callback when a message is received"""
    if mqtt.topic_matches_sub(target_topic_filter, message.topic):
        try:
            message_payload = message.payload.decode("utf-8")
            payload_data = json.loads(message_payload)  

            if isinstance(payload_data, bool) and payload_data:  # If True, stop the production line
                mqtt_client.publish(f"{MQTT_LINE_BASIC_TOPIC}/command", "STOP")
                print("Production Line deactivated")
                
            # print(f"Message received {message.topic}: {payload_data}")

        except json.JSONDecodeError:
            print("Error decoding JSON payload.")

# Assign callbacks to the MQTT client
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

# Connect to the broker
mqtt_client.connect(broker_ip, broker_port)

# Start the MQTT loop (blocking)
mqtt_client.loop_forever()