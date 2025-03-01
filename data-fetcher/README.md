# MQTT Data Fetcher

## Introduction

The **MQTT Data Fetcher** microservice serves as an integration layer between an MQTT broker and an HTTP-based API, using the Paho MQTT library. Its main purpose is to subscribe to specific MQTT topics, process incoming messages, and interact with the Inventory API. Below are the key features implemented:

- **MQTT Topic Subscription**:  
  Subscribes to MQTT topics matching the pattern `robot/+/telemetry/#`.

- **Message Processing and HTTP Integration**:  
  Processes incoming MQTT messages and sends appropriate HTTP requests to the Inventory API.

- **Updating Joint Consumptions**:  
  Sends POST requests to the Inventory API to update consumption data for individual robot joints.

- **Weight Evaluation**:  
  Calculates the weight being carried by the robot's end effector based on the received telemetry data.

- **Updating End Effector Load**:  
  Sends POST requests to update the weight supported by the robot's end effector.

## Methods and Code Structure

To achieve the functionalities mentioned above, we have structured the service with an initialization code and two main methods.

### Initialization

The initialization is done by providing a configuration for HTTP communication and the MQTT client through the `fetcher_conf.yaml` file.
The configuration file information is retrieved using the `read_configuration_file()` method.

To ensure a more robust approach, we also provide the service with a default configuration:

```python
configuration_dict = {
    "broker_ip": "127.0.0.1",
    "broker_port": 1883,
    "target_telemetry_topic": "robot/+/telemetry/#",
    "device_api_url": "http://127.0.0.1:7070/api/v1/productionline/robot"
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
        client.subscribe(info_topic)
```

#### On_message

The on_message function uses a TRY/EXCEPT structure to prevent issues.
If an error occurs, an error log is generated to help the user understand what went wrong.

```python
    def on_message(client, userdata, msg):
        if mqtt.topic_matches_sub(mqtt_topic, msg.topic):
            try:
                ....
            except Exception as e:
                print(f"Error processing MQTT message: {str(e)}")
        if mqtt.topic_matches_sub(info_topic, msg.topic):
            try:
                ....
            except Exception as e:
                print(f"Error processing MQTT message: {str(e)}")
```

Otherwise, it proceeds to elaborate the incoming data and build up the HTTP post request to update the desired quantity.

#### Message handling

We have provided the services with an error management funtion that return error logs if the messages contain some wrong data.

##### Joint Consumption

If the message type is "joints_consumption", a POST request is sent to the API to update the joint consumption data:

```python
    if message == "joints_consumption":
        target_url = f"{api_url}/{robot_id}/telemetry/joints_consumption"
        payload_desired = {
                ...
        }
        response = requests.post(target_url, json=payload_desired)
        print(f"POST request to {target_url} with payload {payload} returned {response.status_code}")
        time.sleep(1)
```

##### Grip (End Effector Weight)

If the message type is "grip", the service calculates the weight carried by the end effector and sends a POST request to update this information:

```python
elif message == "grip":
      target_url = f"{api_url}/{robot_id}/telemetry/weight_ee"

      ... calculations ...

      # Creazione del payload desiderato
      payload_desired = {
          ...
      }
      response = requests.post(target_url, json=payload_desired)
      print(f"POST request to {target_url} with payload {weight} returned {response.status_code}")
      time.sleep(1)
```

##### Unknown Messages

If the message type is unknown, an error is logged:

```python
else:
  print(f"Unknown message type: {message}")
```

##### Production Line Info

If the topic matches, an HTTP POST request is sent to the specified URL to update the production line information. This message is retained by the broker, ensuring that even if no subscribers are currently registered, the last message remains stored. When a new subscriber subscribes to the topic, the broker automatically delivers the most recent message.

```python
if mqtt.topic_matches_sub(info_topic, msg.topic):
        try:
            payload = json.loads(msg.payload.decode())
            target_url = f"{api_url}/robots"
            response = requests.post(target_url, json=payload)
            print(f"POST request to {target_url} with payload {payload} returned {response.status_code}")
        except Exception as e:
            print(f"Error processing MQTT message: {str(e)}")
```

## Running the Service

### Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python data_fetcher.py
   ```

### Dockerized

1. Build the Docker image:
   ```bash
   docker build -t data-fetcher:0.1 .
   ```

## Deployment in Docker Compose

To integrate this microservice into a Docker Compose setup, ensure the following entry exists in `docker-compose.yml`:

```yaml
mqtt_data_fetcher:
  container_name: mqtt_data_fetcher
  image: data-fetcher:0.1
  volumes:
    - ./target_fetcher_conf.yaml:/app/fetcher_conf.yaml
  restart: always
  depends_on:
    - cloud-mosquitto-broker
    - http-api
  networks:
    - iot_production_line_network
```
