# MQTT Production Line

This project simulates a production line using MQTT (Message Queuing Telemetry Transport) for communication between various components such as robot arms, joints, and sensors. The system consists of two main components: the `producer`, which simulates the production process and sends data, and the `consumer`, which receives and processes the data.

## Project Structure

### Producer

The `producer` component is responsible for simulating the production line and publishing data to the MQTT broker.

#### Main Script

- **`production_line_producer.py`**: The core script that simulates the production process and publishes data to the MQTT broker.

#### Key Methods

- `publish_data()`: Publishes data to the MQTT broker.
- `connect_broker()`: Establishes a connection to the MQTT broker.
- `disconnect_broker()`: Terminates the connection with the MQTT broker.
- `simulate_production_line()`: Simulates the production line operations, generating and sending data at regular intervals.

#### Usage

To run the producer, execute the following command:

```bash
python production_line_producer.py
```

### Consumer

The `consumer` component subscribes to the MQTT broker, processes incoming data, and can trigger various actions based on the received messages.

#### Main Script

- **`production_line_consumer.py`**: The core script responsible for subscribing to the MQTT topics and processing incoming messages.

#### Key Methods

- `subscribe_to_topics()`: Subscribes to relevant MQTT topics.
- `process_message()`: Handles incoming messages from the production line.
- `connect_broker()`: Establishes a connection to the MQTT broker.
- `disconnect_broker()`: Terminates the connection with the MQTT broker.

#### Usage

To run the consumer, execute the following command:

```bash
python production_line_consumer.py
```
