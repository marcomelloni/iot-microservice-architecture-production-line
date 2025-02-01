# MQTT Cloud Broker - Eclipse Mosquitto

## Introduction

To facilitate communication between our Dockerized application and the local application simulating the assembly line, we set up an MQTT broker within the Docker environment.
This broker exposes port 1883 to the outside world, enabling external interactions. Additionally, we utilize the default MQTT Bridge functionality to link the local broker to the cloud broker.

## Cloud Broker Setup

The MQTT cloud broker is responsible for collecting incoming data from external sources and relaying it to the appropriate services. While data is published to specific topics on the local broker network, the bridge functionality ensures that these same topics and their contents are made available on the cloud broker inside the Docker network.
Different services interact with these topics to exchange data between the local and cloud networks. In our application, we have two primary services that use these topics:

1. **mqtt_data_fetcher**: This service processes data from the `robot/+/telemetry/joints_consumption` and `robot/+/telemetry/grip_ee` topics and publishes the results to the `robot/<robotId>/data/joints_consumption` and `robot/<robotId>/data/weight_ee` topics.

2. **fault-prevention-actuator**: This service analyzes data published on the `robot/+/data/joints_consumption` and `robot/+/data/weight_ee` topics. Based on this data, it publishes a stop command to the `production_line/control/stop` topic, halting the local production line if needed.

## Mosquitto Broker

For this setup, we use the official Eclipse Mosquitto Broker image from Docker Hub. The specific image and version used in this project are:

- **Image**: `eclipse-mosquitto`
- **Version**: `2.0.12`
- **Docker Hub Link**: [eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto)

## Configuration File

Below is the configuration file for the cloud broker setup:

```bash
listener 1883                        # Expose port 1883 for communication
allow_anonymous true                 # Allow anonymous connections (no authentication required)

# Bridge configuration to connect to the local broker
connection local-mosquitto-broker    # Name for the local broker connection
address 192.168.0.231:1883           # IP address and port of the local broker

# Topic subscription and publishing configuration
topic # in 0                         # Subscribe to all incoming topics
topic # out 0                        # Publish to all outgoing topics

bridge_attempt_unsubscribe false     # Keep the subscription active permanently
try_private false                    # Disable private topics
start_type automatic                 # Automatically start the bridge connection
```

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
