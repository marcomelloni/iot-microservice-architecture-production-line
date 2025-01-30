# For this example we rely on the Paho MQTT Library for Python
# You can install it through the following command: pip install paho-mqtt

from model.production_line import ProductionLine
from model.message_descriptor import MessageDescriptor
import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# Configuration variables
device_id = "test_device_1"
client_id = "ProductionLine0001-Producer"
broker_ip = "127.0.0.1"
broker_port = 1883
joints_consumption_topic = "robot/{}/telemetry/joints_consumption".format(device_id)
grip_topic = "robot/{}/telemetry/grip".format(device_id)
message_limit = 1000

mqtt_client = mqtt.Client(client_id)
mqtt_client.on_connect = on_connect

print("Connecting to " + broker_ip + " port: " + str(broker_port))
mqtt_client.connect(broker_ip, broker_port)

mqtt_client.loop_start()

# Create Demo Production Line
productionline = ProductionLine()

for message_id in range(message_limit):
    productionline.measure_temperature()
    payload_string = MessageDescriptor(int(time.time()), "TEMPERATURE_SENSOR", productionline.temperature_value).to_json()
    infot = mqtt_client.publish(joints_consumption_topic, payload_string)
    infot.wait_for_publish()
    print(f"Message Sent: {message_id} Topic: {joints_consumption_topic} Payload: {payload_string}")
    time.sleep(5)

mqtt_client.loop_stop()
