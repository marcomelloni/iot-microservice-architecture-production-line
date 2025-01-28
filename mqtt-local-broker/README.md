# MQTT Local Broker - Eclipse Mosquitto

## Introduction

In an IoT architecture, it is common to have a **local MQTT broker** handling communication between devices on the local network, while data can be sent to a **remote Cloud MQTT broker** for processing and storage. Using a local broker reduces latency for local devices, while the bridge allows synchronization of data with the cloud.

### Why a Local Broker?

The local broker (Mosquitto) is used to manage MQTT communication within the local network, with significant benefits:

- **Low latency**: Communication between local devices is faster since it doesn't require sending data to an external server (cloud).
- **Independence from Cloud**: If the cloud connection is lost, the local broker can continue to operate and accumulate messages until the connection is restored.
- **Security and privacy**: Local data can be handled without needing to be sent immediately to external servers.

### Bridge Between Local and Cloud Broker

To synchronize data between the local broker and the remote broker in the cloud, we use a "bridge". The bridge allows the local broker to send and receive messages from the remote broker.

- The **bridge** is configured in the `mosquitto_local.conf` file and enables the local broker to forward messages to the cloud broker and vice versa.
- **When the local broker is unreachable from the cloud**, messages are temporarily stored in the local broker and sent when the connection to the cloud is restored.

### Explanation of the `mosquitto_local.conf` Configuration File

The `mosquitto_local.conf` configuration file defines how the local broker connects to the remote broker in the cloud. Below is an explanation of the main parameters:

```bash
connection bridge_to_cloud
```

This parameter defines the name of the bridge connection to the remote cloud broker. The name bridge_to_cloud can be used to reference this connection within the configuration.

```bash
address cloud-mosquitto-broker:1883
```

Specifies the address and port of the remote broker in the cloud. In this case, cloud-mosquitto-broker is the service or Docker container name hosting the MQTT broker in the cloud, and the port is 1883, the default port for Mosquitto.

```bash
topic # both 0
```

Defines the topics that the bridge connects to. The # character indicates that all topics are included (essentially, the local broker both publishes and subscribes to all topics). The number 0 following both specifies the Quality of Service (QoS) level, which in this case is 0 (meaning the message is sent once, without guaranteeing delivery).

```bash
try_private false
```

Sets this option to false, meaning Mosquitto will not attempt to use a private session for the bridge. This means a new session will be created every time the bridge connects.

```bash
start_type automatic
```

Indicates that the bridge should start automatically when Mosquitto starts. This means the connection does not need to be manually initiated.

```bash
cleansession true
```

Sets cleansession to true, meaning the session will be cleared each time the client (or the bridge) disconnects. This removes any prior session information, such as pending messages and subscriptions.

### How the Bridge Works

- Initial Connection: The local broker (Mosquitto) starts up and attempts to connect to the remote broker in the cloud.
- Sending and Receiving Messages: Once the connection is established, all messages published on the local broker to certain topics are also sent to the remote broker, and vice versa.
- Disconnection and Reconnection: If the remote broker is unavailable, messages are stored in the local broker until the connection is restored.

### Running Mosquitto Locally

To start the local MQTT broker using Docker, use the following docker run command.

##### General Version

```bash
docker run --name=my-mosquitto-broker \
  -p 1883:1883 \
  -v ${PWD}/mqtt-local-broker/mosquitto_local.conf:/mosquitto/config/mosquitto.conf \
  -v ${PWD}/docker-compose/data:/mosquitto/data \
  -v ${PWD}/docker-compose/log:/mosquitto/log \
  --restart always \
  -d eclipse-mosquitto:2.0.12
```

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

Parameter Descriptions

- --name=my-mosquitto-broker: Sets the container name as my-mosquitto-broker.
- -p 1883:1883: Maps the container's port 1883 to the host's port 1883. This allows access to the MQTT broker on your host at port 1883.
- -v ${PWD}/mqtt-local-broker/mosquitto_local.conf:/mosquitto/config/mosquitto.conf: Mounts your local mosquitto_local.conf configuration file into the container.
- -v ${PWD}/docker-compose/data:/mosquitto/data: Mounts the data directory to store the broker's persistent data.
- -v ${PWD}/docker-compose/log:/mosquitto/log: Mounts the log directory for broker logs.
- --restart always: Configures the container to automatically restart in case of failure or when the system is rebooted.
- -d: Runs the container in detached mode (in the background).
