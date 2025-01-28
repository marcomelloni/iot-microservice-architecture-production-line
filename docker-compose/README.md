docker run --name=cloud-mosquitto-broker \
 -p 1884:1883 \
 -v "$(pwd)/mqtt-cloud-broker/mosquitto_cloud.conf:/mosquitto/config/mosquitto.conf" \
  -v "$(pwd)/docker-compose/data:/mosquitto/data" \
 -v "$(pwd)/docker-compose/log:/mosquitto/log" \
 --restart always \
 -d eclipse-mosquitto:2.0.12
