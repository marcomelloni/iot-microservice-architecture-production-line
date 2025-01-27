# IoT Microservice Architecture for Production Line Monitoring

This project implements an **IoT Microservices Software Architecture** designed to monitor a production line composed of multiple robotic arms. The architecture leverages microservices and containerization to provide a modular, scalable, and maintainable solution for real-time monitoring and management.

![IoT Architecture](images/iot_architecture.jpg)

## System Overview

The system consists of several key components, each responsible for specific functionalities to ensure seamless integration and operation:

### MQTT Local Broker

Positioned close to the production line, the **MQTT Local Broker** collects data from the robotic arms and forwards it to the **Cloud Broker**. This ensures low-latency communication and efficient data handling within the production environment.

### MQTT Cloud Broker

The **MQTT Cloud Broker** serves as a central hub for data aggregation, receiving messages from the Local Broker and distributing them to subscribed clients. This enables real-time monitoring and analytics from remote locations.

### IoT Inventory

The **IoT Inventory** module, accessed via an HTTP API, manages key robotic arm metrics such as:

- The weight supported by the end effector.
- Power consumption for each robotic arm joint.

It also facilitates interaction with the **MQTT Data Fetcher** for seamless data synchronization.

### MQTT Data Fetcher

This microservice bridges MQTT communication with the **IoT Inventory API**. It subscribes to MQTT topics, processes incoming telemetry data, and interacts with the Inventory system. Additionally, it converts grip sensor values into weight measurements, enabling precise load tracking.

### Web UI

A user-friendly **Web Interface** provides real-time visualization of the production line. Key features include:

- Displaying the power consumption of individual robotic arm joints.
- Showing the weight currently supported by each robotic arm's end effector.

---

## Docker Network

Since we are going to deploy multiple containers, we need to create a dedicated network to allow communication between them.
**In this way containers can communicate with each other using the container name as the hostname.**
This approach will simplify the configuration and the deployment of the services instead of using the IP address of the host machine.

Create a Docker network to allow the containers to communicate with each other:

```bash
  docker network create iot_production_line_network
```

Listing the networks:

```bash
  docker network ls
```

All the containers that we are going to build and deploy will be connected to this network to allow communication between them.
In order to connect a container to a network, you can use the following parameter `--network iot_iot_production_line_network` at the run time:

```bash
  docker run --name=<container_name> --network iot_production_line_network <other_options> <image_name>
```
