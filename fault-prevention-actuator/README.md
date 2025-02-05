# MQTT Data Fetcher

## Introduction

The **Fault Prevention Actuator** microservice serves as a protection layer for the local production line. Its main purpose is to subscribe to specific MQTT topic, process incoming messages, and interact with the production line, notifying every problem discovered at the user through the HTTP-API. Below are the key features implemented:

- **MQTT Topic Subscription**:  
  Subscribes to MQTT topics matching the pattern `robot/+/telemetry/#`.

- **Message Processing and Monitoring**:  
  Processes incoming MQTT messages and monitor when the production line need to be stopped allowing for a robot maintenance.

- **Updating Joint Consumptions**:  
  Sends POST requests to the Inventory API to update consumption data for individual robot joints.

## Methods and Code Structure

To achieve the functionalities mentioned above, we have structured the service with an initialization code and different methods.

### Initialization

The initialization is done by providing a configuration for the MQTT client through the `actuator_conf.yaml` file.
The configuration file information is retrieved using the `read_configuration_file()` method.

To ensure a more robust approach, we also provide the service with a default configuration:

```python
configuration_dict = {
    "broker_ip": "127.0.0.1",
    "broker_port": 1883,
    "target_telemetry_topic": "robot/+/telemetry/#"
}
```

### MQTT Functions

Furthermore, we have written the basic MQTT functions to customize the behaviour of the service to achieve the fixed goals.

#### On_connect

The on_connect function is triggered when the service successfully connects to the MQTT broker.
We use it to notify the user of the successful connection and to have the service subscribe to the desired topics.

```python
    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT Broker with result code " + str(rc))
        client.subscribe(mqtt_topic)

```

#### On_message

The `on_message` function uses a TRY/EXCEPT structure to check if the incoming message is of the "joints_consumption" type. If an error occurs, an error log is generated to help the user understand what went wrong.

```python
    def on_message(client, userdata, msg):
        if mqtt.topic_matches_sub(mqtt_topic, msg.topic):
            try:
                ....
            except Exception as e:
                print(f"Error processing MQTT message: {str(e)}")
```

Otherwise, it proceeds to elaborate the incoming data and test the worn out condition.

#### Message handling

We have provided the services with an error management function that return error logs if the messages contain some wrong data.

##### Joint Consumption

If the message type is "joints_consumption," the joint consumption data is extracted, and the worn-out condition is tested.
In case a problem is discovered, the service deliver a stop order to the local production line through the MQTT cloud broker, publishing the command on the
To ensure reliable message reception between the Actuator service and teh local production line, the Quality of Service (QoS) is set to `QOS2`.

```python
            if message == "joints_consumption":
                # Extract joint consumption data from the payload
                for sensor in payload.get('joint_consumption_sensors', []):
                    for joint in sensor.get('joints', []):
                        consumption = ...
                        ...
                        if consumption > 100:
                            ...
                            client.publish(mqtt_topic_publish, json.dumps(value), qos=2)
                            print(f"Published message to {mqtt_topic_publish} with payload {value} because {robot_id} - {joint_id} consumed {consumption} kW")

                            timenow = datetime.now()
                            target_url = f"{api_url}/faults"
                            payload_desired = {
                                ...
                            }

                            response = requests.post(target_url, json=payload_desired)
                            print(f"POST request to {target_url} with payload {payload} returned {response.status_code}")
```

##### Unknown Messages

If the message type is unknown, an error is logged:

```python
            else:
                print(f"Unknown message type: {message}")
```
