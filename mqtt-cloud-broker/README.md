# MQTT Cloud Broker - Eclipse Moquitto

In this configuration we are going to use the default Eclipse Mosquitto Broker already available on Docker Hub at the following link: [https://hub.docker.com/\_/eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto)

The target used image and version for this playground is: `eclipse-mosquitto:2.0.12`

The resulting Run command is (In case of Linux System) :

```bash
docker run --name=cloud-mosquitto-broker \
 -p 1884:1883 \
 -v "$(pwd)/mqtt-cloud-broker/mosquitto_cloud.conf:/mosquitto/config/mosquitto.conf" \
  -v "$(pwd)/docker-compose/data:/mosquitto/data" \
 -v "$(pwd)/docker-compose/log:/mosquitto/log" \
 --restart always \
 -d eclipse-mosquitto:2.0.12

```
