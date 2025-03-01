# MQTT Data Fetcher

## Introduction

The **Fault Prevention Actuator** microservice serves as a protection layer for the local production line. Its main
purpose is to subscribe to specific MQTT topic, process incoming messages, and interact with the production line,
notifying every problem discovered at the user through the HTTP-API. Below are the key features implemented:

- **MQTT Topic Subscription**:  
  Subscribes to MQTT topics matching the pattern `robot/+/telemetry/#`.

- **Real Time Data Processing**:  
  Processes incoming MQTT messages and checks for worn-out conditions in the robot joints.

- **Faults Message Storage**:  
  Sends POST requests to the HTTP-API to save the faults detected in the production line.

## Methods and Code Structure

To achieve the functionalities mentioned above, we have structured the service with an initialization code and different
methods.

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

Furthermore, we have written the basic MQTT functions to customize the behaviour of the service to achieve the fixed
goals.

#### On_connect

The on_connect function is triggered when the service successfully connects to the MQTT broker.
We use it to notify the user of the successful connection and to have the service subscribe to the desired topics.

```python
    def on_connect(client, userdata, flags, rc):


print("Connected to MQTT Broker with result code " + str(rc))
client.subscribe(mqtt_topic)

```

#### On_message

The `on_message` function uses a TRY/EXCEPT structure to check if the incoming message is of the "joints_consumption"
type. If an error occurs, an error log is generated to help the user understand what went wrong.

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

We have provided the services with an error management function that return error logs if the messages contain some
wrong data.

##### Joint Consumption

If the message type is "joints_consumption," the joint consumption data is extracted, and the worn-out condition is
tested.
In case a problem is discovered, the service deliver a stop order to the local production line through the MQTT cloud
broker, publishing the command on the
To ensure reliable message reception between the Actuator service and the local production line, the Quality of
Service (QoS) is set to `QOS2`.

```python
        if message == "joints_consumption":
            # Extract joint consumption data from the payload
            if payload.get('joint_consumption_sensors'):
                # Loop through the joint consumption sensors data
                for sensor in payload['joint_consumption_sensors']:
                    # Extract joint_id and its consumption
                    joint_id = sensor.get('joint_id', 'N/A')
                    current_sensor = sensor.get('current_sensor', {})
                    consumption = current_sensor.get('value', 0.0)  # Get the current consumption value

                    if consumption > 100:
                        # If consumption exceeds 100, send a stop signal to the production line
                        mqtt_topic_publish = "production_line/control/stop"
                        value = True
                        client.publish(mqtt_topic_publish, json.dumps(value), qos=2)
                        print(f"Published message to {mqtt_topic_publish} with payload {value} because {joint_id} consumed {consumption} A")
                        
                        ...
                        
                        # Prepare the POST request payload
                        target_url = f"{api_url}/faults"
                        payload_desired = {
                            "robot_id": payload.get('robot_arm_id', 'N/A'),
                            "fault": f"Robot {payload.get('robot_arm_id', 'N/A')} - Joint {joint_id} consumed {consumption} A at {timenow}"
                        }

                        # Send the fault report via POST request
                        response = requests.post(target_url, json=payload_desired)
                        print(
                            f"POST request to {target_url} with payload {payload_desired} returned {response.status_code}")

                        return
```

## Running the Service

### Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python fault_prevention_actuator.py
   ```

### Dockerized

1. Build the Docker image:
   ```bash
   docker build -t mqtt-fault-actuator:0.1 .
   ```

## Deployment in Docker Compose

To integrate this microservice into a Docker Compose setup, ensure the following entry exists in `docker-compose.yml`:

```yaml
mqtt-fault-actuator:
  container_name: mqtt-fault-actuator
  image: mqtt-fault-actuator:0.1
  volumes:
    - ./target_actuator_conf.yaml:/app/actuator_conf.yaml
  restart: always
  depends_on:
    - cloud-mosquitto-broker
  networks:
    - iot_production_line_network
```
