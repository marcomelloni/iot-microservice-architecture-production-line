# MQTT Data Fetcher

## Introduction

The **MQTT Data Fetcher** microservice acts as an integration layer between an MQTT broker and an HTTP-based API, leveraging the Paho MQTT library. Its main purpose is to subscribe to specific MQTT topics, process incoming messages, and interact with the Inventory API. Below are the key features implemented:

- **MQTT Topic Subscription**:  
  Subscribes to MQTT topics matching the pattern `robot/+/telemetry/#`.

- **Message Processing and HTTP Integration**:  
  Processes incoming MQTT messages and makes appropriate HTTP requests to the Inventory API.

- **Updating Joint Consumptions**:  
  Sends POST requests to the Inventory API to update the consumption data for individual robot joints.

- **Weight Evaluation**:  
  Calculates the weight being carried by the robot's end effector based on the telemetry data received.

- **Updating End Effector Load**:  
  Sends POST requests to update the weight supported by the robot's end effector.
