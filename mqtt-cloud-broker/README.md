# MQTT Cloud Broker - Eclipse Mosquitto

## Introduction

The MQTT Cloud Broker facilitates the aggregation and management of data from local devices. By using Eclipse Mosquitto in the cloud, it ensures efficient communication between local brokers and external systems.

## Cloud Broker Setup

The MQTT cloud broker is responsible for collecting incoming data from external sources and relaying it to the
appropriate services. While data is published to specific topics on the local broker network, the bridge functionality
ensures that these same topics and their contents are made available on the cloud broker inside the Docker network.
Different services interact with these topics to exchange data between the local and cloud networks. In our application,
we have two primary services that use these topics: Data Fetcher and Fault Actuator.

For this setup, we use the official Eclipse Mosquitto Broker image from Docker Hub. The specific image and version used
in this project are:

- **Image**: `eclipse-mosquitto`
- **Version**: `2.0.12`
- **Docker Hub Link**: [eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto)

# mosquitto_cloud.conf: Cloud Broker Configuration

Below is a detailed explanation of the various settings used in the file.

## 1. Listener Configuration

⁠ listener 1883 ⁠

_Description_: This line configures the cloud Mosquitto broker to listen on port 1883. This is the default port for MQTT
communication, and it allows local devices to connect to the broker.

## 2. Allow Anonymous Connections

⁠ allow_anonymous true ⁠

_Description_: This setting allows anonymous connections to the cloud broker. With this configuration, clients do not
need to provide authentication credentials (username and password) to connect to the broker. This can be useful in local
networks where devices are trusted, but it is not recommended for production environments where security is important.

## 3. Bridge Configuration to Local Broker

This section sets up the bridge connection between the cloud broker and the local broker. The bridge allows the cloud
broker to send and receive messages to and from the local one.

### ⁠ connection local-mosquitto-broker ⁠

_Description_: ⁠ local-mosquitto-broker ⁠ is a reference name
that can be used later to configure the connection.

### ⁠ address 192.168.0.231:1883 ⁠

_Description_: This defines the IP address and port of the local broker. In this case, 192.168.0.231 refers to the local machine's IP address where the broker is hosted, and 1883 is the default MQTT port. The cloud broker will use this address to establish a connection and synchronize messages with the local broker.

### ⁠ topic # in 0 ⁠

_Description_: This line defines the topics that the cloud broker subscribes to from the local broker. ⁠ # ⁠ is a
wildcard that indicates all topics are included. ⁠ In 0 ⁠ specifies that messages received from the local broker on
these topics will be processed with a Quality of Service (QoS) level of 0, meaning the message is sent at most once
without any delivery guarantees.

### ⁠ topic # out 0 ⁠

_Description_: This line defines the topics to which the cloud broker will publish messages to the local broker. Again,
⁠ # ⁠ indicates all topics. ⁠ Out 0 ⁠ specifies that messages sent from the cloud broker will be published with QoS 0.

### ⁠ bridge_attempt_unsubscribe false ⁠

_Description_: This parameter specifies whether the cloud broker should attempt to unsubscribe from topics if the bridge
connection is lost. Setting it to ⁠ false ⁠ means that the broker will not attempt to unsubscribe if it fails to do so.

### ⁠ try_private false ⁠

_Description_: This setting specifies whether the bridge should use private topics. Setting it to ⁠ false ⁠ means that
the bridge will not use private sessions, and all sessions will be new for each connection to the local broker.

### ⁠ start_type automatic ⁠

_Description_: This option ensures that the bridge starts automatically when the cloud Mosquitto broker starts. This
means the bridge will not require manual intervention to establish a connection to the local broker.

### ⁠ cleansession true ⁠

_Description_: This sets the session to be clean, meaning that all session data (such as subscriptions) is discarded
when the connection is lost or closed. A new session will be created each time the bridge connects.

## 4. Logging Configuration

### ⁠ log_dest stdout ⁠

_Description_: This line configures the broker to output logs to the standard output (stdout). It helps with
troubleshooting by allowing logs to be visible in the terminal or console where the broker is running.

### ⁠ log_type all ⁠

_Description_: This specifies that all types of logs should be captured. This includes connection logs, message logs,
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
