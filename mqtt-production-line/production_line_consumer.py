import paho.mqtt.client as mqtt
from model.production_line import ProductionLine

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(target_topic_filter)
    print("Subscribed to: " + target_topic_filter)


# Define a callback method to receive asynchronous messages
def on_message(client, userdata, message):

    # If the received message match the target filter
    if mqtt.topic_matches_sub(target_topic_filter, message.topic):
        message_payload = str(message.payload.decode("utf-8"))
        # ferma la linea di produzione


# Configuration variables
client_id = "ProductionLine0001-Consumer"
broker_ip = "127.0.0.1"
broker_port = 1883
target_topic_filter = "production_line/control/stop"

# Create a new MQTT Client
mqtt_client = mqtt.Client(client_id)

# Attack Paho OnMessage Callback Method
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

# Connect to the target MQTT Broker
mqtt_client.connect(broker_ip, broker_port)
mqtt_client.loop_forever()