# Model Directory

This directory contains the core models used in the `mqtt-production-line` project. These models represent various components of the production line, such as robot arms, joints, and sensors.

## Directory Structure

### Files

- **`device.py`**: Defines the base class for all devices in the production line.
- **`joint.py`**: Defines the `Joint` class, representing a joint in a robot arm.
- **`robot_arm.py`**: Defines the `RobotArm` class, representing a robot arm with multiple joints and sensors.
- **`sensor.py`**: Defines the `Sensor` class, representing a generic sensor device.
- **`current_sensor.py`**: Defines the `CurrentSensor` class, a specialized sensor that measures current consumption.
- **`grip_sensor.py`**: Defines the `GripSensor` class, a specialized sensor that measures grip status.
- **`production_line.py`**: Defines the `ProductionLine` class, representing a standard production line.

## Class Overview

### Device

The `Device` class serves as the base class for all devices in the production line, providing common attributes such as:

- `device_id`
- `device_type`
- `device_manufacturer`

### Sensor

The `Sensor` class serves as a generic representation of sensor devices, with attributes and methods including:

- `value`: The measured value from the sensor.
- `unit`: The unit of measurement.
- `timestamp`: The timestamp of the measurement.
- `update_measurement()`: Abstract method to be implemented by subclasses.

### CurrentSensor

The `CurrentSensor` class measures the current consumption of a robot arm's joints. It includes methods to manage automated updates:

- `start_auto_update()`: Starts automatic data collection.
- `stop_auto_update()`: Stops automatic data collection.

### GripSensor

The `GripSensor` class measures the grip status of a robot arm. It includes methods to manage automated updates:

- `start_auto_update()`: Starts automatic data collection.
- `stop_auto_update()`: Stops automatic data collection.

### Joint

The `Joint` class represents a joint in a robot arm and includes methods to reset and manage its state:

- `reset()`: Resets the joint to its default state.
- `get_state()`: Retrieves the current state of the joint.
- `set_state(state)`: Sets the state of the joint.

### RobotArm

The `RobotArm` class represents a robotic arm composed of multiple joints and sensors. It provides methods for component management and data retrieval:

- `add_joint(joint)`: Adds a joint to the robot arm.
- `add_joint_consumption_sensor(sensor)`: Attaches a current consumption sensor.
- `add_grip_sensor(sensor)`: Attaches a grip sensor.
- `reset()`: Resets the robot arm and its components.
- `get_json_joint_consumptions()`: Retrieves joint consumption data in JSON format.
- `get_json_grip()`: Retrieves grip status data in JSON format.

![Robot_arm_class_img](/readme_images/Robotic_arm_scheme.png)

### Production Line Class

Every individual robot arm on the production line can be represented by an instance of the `RobotArm` class.  
To manage multiple `RobotArm` instances, make all of them communicate with the MQTT broker, and listen to commands like `START` and `STOP`, we have decided to realize another class called "Production line".  
This super-class collects and publishes telemetry data such as joint consumption and grip force for each robot arm.

#### Methods:

- `__init__(self, line_id: str)`: Initializes the production line with a unique ID.
- `add_robot_arm(self, robot_arm: RobotArm)`: Adds a robot arm to the production line.
- `deactivate(self)`: Deactivates the production line and stops all robot arms.
- `activate(self)`: Activates the production line and starts all robot arms.
- `on_connect(self, client, userdata, flags, rc)`: Callback method when the MQTT connection is established.
- `publish_measurement(self, sensor_data: Dict, topic: str)`: Publishes telemetry data (e.g., joint consumption, grip) to an MQTT topic.
- `on_message(self, client, userdata, msg)`: Handles incoming MQTT messages, such as "START" and "STOP".
- `start_mqtt_client(self)`: Initializes and starts the MQTT client with command subscription and a Last Will message.
- `stop_mqtt_client(self)`: Stops the MQTT client and sends a Last Will message.
- `monitor_and_publish(self)`: Simulates monitoring and publishing data from the robot arms.

#### Production Line MQTT Integration

The MQTT communication is controlled and monitored using the `paho.mqtt` library for generating a standard MQTT client to interact with the local broker.

##### MQTT Broker Configuration
The MQTT broker is configured with the following parameters:

- **Broker Address**: `"0.0.0.0"`
- **Broker Port**: `1883` (default MQTT port)
- **Username**: `"iot-project-Melloni-Angelini-Morselli"`
- **Password**: `"password"`
- **Base Topic**: `"robot"`

##### MQTT Message Flow
The MQTT message flow is managed by the `on_connect()` and `on_message()` default methods. The `on_connect()` method has the duty to advertise the user of the outcome of the connection.

```python
 def on_connect(self, client, userdata, flags, rc):
        """Callback when the MQTT connection is established"""
        if rc == 0:
            self.mqtt_connected = True
            print("Connected to the MQTT broker successfully!")
        else:
            print(f"MQTT connection error: {rc}")
```

Instead, the `on_message()` method has to decode the incoming messages and, based on the message payload, take decisions on whether to stop or start the production line.
The commands contained in the payload can be of only 2 types:

- **`START` Command**:
    - Activates the production line and robot arms if the line is not already active.
    - Starts the MQTT client to receive commands.

- **`STOP` Command**:
    - Deactivates the production line and stops the robot arms if the line is active.
    - Stops the MQTT client and sends a "stopped" status message.

```python

    def on_message(self, client, userdata, msg):
        """Handles incoming MQTT messages"""
        payload = msg.payload.decode("utf-8")
        print(f"[DEBUG] Received message on topic {msg.topic}: {payload}")

        if payload == "STOP":
            if self.stopped:  # Skip if already stopped
                print("[DEBUG] STOP command ignored (already stopped)")
                return
            self.deactivate()  # Stop the production line
            self.stop_mqtt_client()  # Stop the MQTT client
            self.stopped = True  # Mark as stopped
            
        elif payload == "START":
            if not self.stopped:  # Skip if already running
                print("[DEBUG] START command ignored (already running)")
                return
            self.start_mqtt_client()  # Start the MQTT client
            self.activate()  # Restart the production line
            self.stopped = False  # Reset stopped flag
```

####  Adding robot arms to the Production Line
The Production Line class can manage only the robots that are added to it, so to add a robot arm to the class, we have realized the add_robot_arm() method:
```python
    def add_robot_arm(self, robot_arm: RobotArm):
        """Adds a robot arm to the production line"""
        self.robot_arms[robot_arm.arm_id] = robot_arm
```

####  Telemetry Data
The system collects and publishes telemetry data from the robot arms in the following formats:
- **Joint Consumption**: Energy consumption of robot arm joints.
- **Grip**: Grip force applied by the robot arm.

These measurements are sent to topics formatted like:
- robot/<arm_id>/telemetry/joints_consumption
- robot/<arm_id>/telemetry/grip

#### Monitor and Publish Data: 
The system continuously monitors the robot arms and publishes telemetry data while the production line is active. The data is sent over MQTT to the appropriate topics.
The collecting of data is managed by the `monitor_and_publish()` method, this method use a TRY and EXCEPT structure to verify that the production line is currently `Active` and running, then for each robot arm collect data from every joint and the grip sensor.

```python
   def monitor_and_publish(self):
        """Simulates monitoring and publishing MQTT data"""
        self.monitoring_active = True
        try:
            while self.active and self.monitoring_active:
                for robot_arm in self.robot_arms.values():
                   # retrieve data from each sensor
                    payload_joint_consumptions = robot_arm.get_json_consumptions()
                    payload_grip = robot_arm.get_json_grip()

                    topic_joints_consumption = f"{MQTT_BASIC_TOPIC}/{robot_arm.arm_id}/telemetry/joints_consumption"
                    # assembly MQTT topic to publish joint consumption data
                    topic_grip = f"{MQTT_BASIC_TOPIC}/{robot_arm.arm_id}/telemetry/grip"
                    
                    # publish measurements
                    self.publish_measurement(payload_joint_consumptions, topic_joints_consumption)
                    self.publish_measurement(payload_grip, topic_grip)
        except KeyboardInterrupt:
            # Handle graceful exit on user interruption
            print("[DEBUG] Monitoring interrupted by user.")
        except Exception as e:
            # Log unexpected errors
            print(f"[ERROR] An error occurred: {e}")
        finally:
            # Ensure that the MQTT client is stopped, and LWT is sent in any case
            print("[DEBUG] Exiting monitoring loop.")
            self.stop_mqtt_client()  # Ensure LWT message is sent
```

The publishing part is realized by the `publish_measurement()` method:
```python
    def publish_measurement(self, sensor_data: Dict, topic: str):
        """Publishes sensor data to the MQTT topic"""
        if self.mqtt_connected:
            self.mqtt_client.publish(topic, json.dumps(sensor_data), qos=0, retain=False)
        else:
            print("Error: not connected to the MQTT broker.")
```

####  Last Will and Testament (LWT)
To assure a more robust approach, we have provided our system with Last Will and Testament (LWT) messages. This type of message is sent when the MQTT client disconnects unexpectedly, providing a "disconnected" or "stopped" status to the MQTT broker. These messages are published to:

- robot/production-line/status.

The LWT is prepared inside the start_mqtt_client(self) and stop_mqtt_client(self) methods. For each method, we set different LWT messages to handle the different situations that can arise.
```python
    def start_mqtt_client(self):
        """Initializes and starts the MQTT client with command subscription and Last Will message"""
        self.mqtt_client = mqtt.Client(f"production-line-{self.line_id}")
        
        # Set up the Last Will and Testament (LWT) message
        lwt_topic = f"{MQTT_BASIC_TOPIC}/production-line/status"
        lwt_message = json.dumps({"status": "disconnected", "line_id": self.line_id})
        self.mqtt_client.will_set(lwt_topic, payload=lwt_message, qos=1, retain=False)
        
        # Set callback functions for handling MQTT events
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message  # Add message handling function
        
        # Set MQTT credentials
        self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)
        self.mqtt_client.subscribe(f"{MQTT_BASIC_TOPIC}/command")
        self.mqtt_client.loop_start()
        print(f"MQTT client started for production line {self.line_id}")

    def stop_mqtt_client(self):
        """Stops the MQTT client and sends Last Will message"""
        if self.mqtt_client:
            # Send a "stopped" status message if the client disconnects normally
            lwt_topic = f"{MQTT_BASIC_TOPIC}/production-line/status"
            lwt_message = json.dumps({"status": "stopped", "line_id": self.line_id})
            result = self.mqtt_client.publish(lwt_topic, payload=lwt_message, qos=1, retain=False)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[DEBUG] LWT message sent to topic {lwt_topic} with payload {lwt_message}")
            else:
                print(f"[ERROR] Failed to send LWT message, result code: {result.rc}")
```

## Usage

These models define the core components of the production line and are used within the main script `production_line_producer.py` and `production_line_consumer.py`

### Example

Below is an example of how to create a simple production line:

```python

# Robot Creation
robot_arm_1 = RobotArm("RA_001", "XYZ Robotics", 3, 1)
robot_arm_2 = RobotArm("RA_002", "XYZ Robotics", 3, 1)
robot_arm_3 = RobotArm("RA_003", "XYZ Robotics", 3, 1)

# Production Line Creation
production_line = ProductionLine("PL_001")

# Add robot arms to the production line
production_line.add_robot_arm(robot_arm_1)
production_line.add_robot_arm(robot_arm_2)
production_line.add_robot_arm(robot_arm_3)


```
