# MQTT Local Broker - Eclipse Mosquitto

## Introduction

In an IoT architecture, it is common to have a **local MQTT broker** handling communication between devices on the local
network, while data can be sent to a **remote Cloud MQTT broker** for processing and storage. Using a local broker
reduces latency for local devices, while the bridge allows synchronization of data with the cloud.

### Why a Local Broker?

The local broker (Mosquitto) is used to manage MQTT communication within the local network, with significant benefits:

- **Low latency**: Communication between local devices is faster since it doesn't require sending data to an external
  server (cloud).
- **Independence from Cloud**: If the cloud connection is lost, the local broker can continue to operate and accumulate
  messages until the connection is restored.
- **Security and privacy**: Local data can be handled without needing to be sent immediately to external servers.

### Bridge Between Local and Cloud Broker

To synchronize data between the local broker and the remote broker in the cloud, we use a "bridge". The bridge allows
the local broker to send and receive messages from the remote broker.

- The **bridge** is configured in the `mosquitto_local.conf` file and enables the local broker to forward messages to
  the cloud broker and vice versa.
- **When the local broker is unreachable from the cloud**, messages are temporarily stored in the local broker and sent
  when the connection to the cloud is restored.

## mosquitto_local.conf: Local Broker Configuration

This configuration file sets up Mosquitto to run a local MQTT broker, while also establishing a bridge between the local
broker and a remote cloud broker for synchronization. Below is a detailed explanation of the various settings used in
the file.

### 1. Listener Configuration

⁠ listener 1883 ⁠

*Description*: This line configures the local Mosquitto broker to listen on port 1883. This is the default port for MQTT
communication, and it allows local devices to connect to the broker.

### 2. Allow Anonymous Connections

⁠ allow_anonymous true ⁠

*Description*: This setting allows anonymous connections to the local broker. With this configuration, clients do not
need to provide authentication credentials (username and password) to connect to the broker. This can be useful in local
networks where devices are trusted, but it is not recommended for production environments where security is important.

### 3. Bridge Configuration to Cloud Broker

This section sets up the bridge connection between the local broker and the cloud broker. The bridge allows the local
broker to send and receive messages to and from the cloud.

#### ⁠ connection cloud-mosquitto-broker ⁠

*Description*: This parameter defines the name of the bridge connection. ⁠ cloud-mosquitto-broker ⁠ is a reference name
that can be used later to configure the connection.

#### ⁠ address 172.18.0.2:1883 ⁠

*Description*: This specifies the address and port of the cloud broker. In this case, ⁠ 172.18.0.2 ⁠ is the IP address
of the cloud broker (it could be a Docker container or a remote server), and ⁠ 1883 ⁠ is the default MQTT port. The
local broker will attempt to connect to this IP address to synchronize messages.

#### ⁠ topic # in 0 ⁠

*Description*: This line defines the topics that the local broker subscribes to from the cloud broker. ⁠ # ⁠ is a
wildcard that indicates all topics are included. ⁠ in 0 ⁠ specifies that messages received from the cloud broker on
these topics will be processed with a Quality of Service (QoS) level of 0, meaning the message is sent at most once
without any delivery guarantees.

#### ⁠ topic # out 0 ⁠

*Description*: This line defines the topics to which the local broker will publish messages to the cloud broker. Again,
⁠ # ⁠ indicates all topics. ⁠ out 0 ⁠ specifies that messages sent from the local broker will be published with QoS 0.

#### ⁠ bridge_attempt_unsubscribe false ⁠

*Description*: This parameter specifies whether the local broker should attempt to unsubscribe from topics if the bridge
connection is lost. Setting it to ⁠ false ⁠ means that the broker will not attempt to unsubscribe if it fails to do so.

#### ⁠ try_private false ⁠

*Description*: This setting specifies whether the bridge should use private topics. Setting it to ⁠ false ⁠ means that
the bridge will not use private sessions, and all sessions will be new for each connection to the cloud broker.

#### ⁠ start_type automatic ⁠

*Description*: This option ensures that the bridge starts automatically when the local Mosquitto broker starts. This
means the bridge will not require manual intervention to establish a connection to the cloud broker.

#### ⁠ cleansession true ⁠

*Description*: This sets the session to be clean, meaning that all session data (such as subscriptions) is discarded
when the connection is lost or closed. A new session will be created each time the bridge connects.

### 4. Logging Configuration

#### ⁠ log_dest stdout ⁠

*Description*: This line configures the broker to output logs to the standard output (stdout). It helps with
troubleshooting by allowing logs to be visible in the terminal or console where the broker is running.

#### ⁠ log_type all ⁠

*Description*: This specifies that all types of logs should be captured. This includes connection logs, message logs,
error logs, and more. It helps track all broker activity for debugging and monitoring.

#### How the Bridge Works

- Initial Connection: The local broker (Mosquitto) starts up and attempts to connect to the remote broker in the cloud.
- Sending and Receiving Messages: Once the connection is established, all messages published on the local broker to
  certain topics are also sent to the remote broker, and vice versa.
- Disconnection and Reconnection: If the remote broker is unavailable, messages are stored in the local broker until the
  connection is restored.

## Running Mosquitto Locally

To start the local MQTT broker using Docker, use the following docker run command.

##### Linux Version

```bash
docker run --name=my-mosquitto-broker \
  -p 1883:1883 \
  -v "$(pwd)/mqtt-local-broker/mosquitto_local.conf:/mosquitto/config/mosquitto.conf" \
  -v "$(pwd)/docker-compose/data:/mosquitto/data" \
  -v "$(pwd)/docker-compose/log:/mosquitto/log" \
  --restart always \
  -d eclipse-mosquitto:2.0.12

```

##### Windows Version

```bash
docker run --name my-mosquitto-broker `
  -p 1883:1883 `
  -v "${PWD}/mqtt-local-broker/mosquitto_local.conf:/mosquitto/config/mosquitto.conf" `
  -v "${PWD}/docker-compose/data:/mosquitto/data" `
  -v "${PWD}/docker-compose/log:/mosquitto/log" `
  --restart always `
  -d eclipse-mosquitto
```

Parameter Descriptions

- --name=my-mosquitto-broker: Sets the container name as my-mosquitto-broker.
- -p 1883:1883: Maps the container's port 1883 to the host's port 1883. This allows access to the MQTT broker on your
  host at port 1883.
- -v ${PWD}/mqtt-local-broker/mosquitto_local.conf:/mosquitto/config/mosquitto.conf: Mounts your local
  mosquitto_local.conf configuration file into the container.
- -v ${PWD}/docker-compose/data:/mosquitto/data: Mounts the data directory to store the broker's persistent data.
- -v ${PWD}/docker-compose/log:/mosquitto/log: Mounts the log directory for broker logs.
- --restart always: Configures the container to automatically restart in case of failure or when the system is rebooted.
- -d: Runs the container in detached mode (in the background).
