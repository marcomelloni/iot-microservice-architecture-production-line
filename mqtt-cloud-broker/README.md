# MQTT Cloud Broker - Eclipse Mosquitto

## Introduction

To facilitate communication between our Dockerized application and the local application simulating the assembly line,
we set up an MQTT broker within the Docker environment.
This broker exposes port 1883 to the outside world, enabling external interactions. Additionally, we utilize the default
MQTT Bridge functionality to link the local broker to the cloud broker.

## Cloud Broker Setup

The MQTT cloud broker is responsible for collecting incoming data from external sources and relaying it to the
appropriate services. While data is published to specific topics on the local broker network, the bridge functionality
ensures that these same topics and their contents are made available on the cloud broker inside the Docker network.
Different services interact with these topics to exchange data between the local and cloud networks. In our application,
we have two primary services that use these topics:

1. **mqtt_data_fetcher**

2. **fault-prevention-actuator**

## Mosquitto Broker

For this setup, we use the official Eclipse Mosquitto Broker image from Docker Hub. The specific image and version used
in this project are:

- **Image**: `eclipse-mosquitto`
- **Version**: `2.0.12`
- **Docker Hub Link**: [eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto)

## Configuration File

# mosquitto_cloud.conf: Cloud Broker Configuration
Below is a detailed explanation of the various settings used in the file.

## 1. Listener Configuration

⁠ listener 1883 ⁠

*Description*: This line configures the local Mosquitto broker to listen on port 1883. This is the default port for MQTT
communication, and it allows local devices to connect to the broker.

## 2. Allow Anonymous Connections

⁠ allow_anonymous true ⁠

*Description*: This setting allows anonymous connections to the local broker. With this configuration, clients do not
need to provide authentication credentials (username and password) to connect to the broker. This can be useful in local
networks where devices are trusted, but it is not recommended for production environments where security is important.

## 3. Bridge Configuration to Local Broker

This section sets up the bridge connection between the cloud broker and the local broker. The bridge allows the cloud
broker to send and receive messages to and from the local one.

### ⁠ connection local-mosquitto-broker ⁠

*Description*: This parameter defines the name of the bridge connection. ⁠ local-mosquitto-broker ⁠ is a reference name
that can be used later to configure the connection.

### ⁠ address 192.168.0.231:1883 ⁠

*Description*: This specifies the address and port of the local broker. In this case, ⁠ 192.168.0.231 ⁠ is the IP address
of the local broker (it could be a Docker container or a remote server), and ⁠ 1883 ⁠ is the default MQTT port. The
cloud broker will attempt to connect to this IP address to synchronize messages.

### ⁠ topic # in 0 ⁠

*Description*: This line defines the topics that the cloud broker subscribes to from the local broker. ⁠ # ⁠ is a
wildcard that indicates all topics are included. ⁠ in 0 ⁠ specifies that messages received from the local broker on
these topics will be processed with a Quality of Service (QoS) level of 0, meaning the message is sent at most once
without any delivery guarantees.

### ⁠ topic # out 0 ⁠

*Description*: This line defines the topics to which the cloud broker will publish messages to the local broker. Again,
⁠ # ⁠ indicates all topics. ⁠ out 0 ⁠ specifies that messages sent from the cloud broker will be published with QoS 0.

### ⁠ bridge_attempt_unsubscribe false ⁠

*Description*: This parameter specifies whether the cloud broker should attempt to unsubscribe from topics if the bridge
connection is lost. Setting it to ⁠ false ⁠ means that the broker will not attempt to unsubscribe if it fails to do so.

### ⁠ try_private false ⁠

*Description*: This setting specifies whether the bridge should use private topics. Setting it to ⁠ false ⁠ means that
the bridge will not use private sessions, and all sessions will be new for each connection to the local broker.

### ⁠ start_type automatic ⁠

*Description*: This option ensures that the bridge starts automatically when the cloud Mosquitto broker starts. This
means the bridge will not require manual intervention to establish a connection to the local broker.

### ⁠ cleansession true ⁠

*Description*: This sets the session to be clean, meaning that all session data (such as subscriptions) is discarded
when the connection is lost or closed. A new session will be created each time the bridge connects.

## 4. Logging Configuration

### ⁠ log_dest stdout ⁠

*Description*: This line configures the broker to output logs to the standard output (stdout). It helps with
troubleshooting by allowing logs to be visible in the terminal or console where the broker is running.

### ⁠ log_type all ⁠

*Description*: This specifies that all types of logs should be captured. This includes connection logs, message logs,
error logs, and more. It helps track all broker activity for debugging and monitoring.

## Run Command

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
