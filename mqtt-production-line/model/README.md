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

## Usage

These models define the core components of the production line and are used within the main script (`production_line_producer.py`).

### Example

Below is an example of how to create a robot arm and add joints and sensors to it:

```python
from model.robot_arm import RobotArm
from model.joint import Joint
from model.current_sensor import CurrentSensor
from model.grip_sensor import GripSensor

# Create joints
joint_1 = Joint("J1")
joint_2 = Joint("J2")

# Create a robot arm
robot_arm = RobotArm("RA_001", "XYZ Robotics")

# Add joints to the robot arm
robot_arm.add_joint(joint_1)
robot_arm.add_joint(joint_2)

# Create sensors
current_sensor = CurrentSensor("CS_001", "XYZ Robotics", robot_arm)
grip_sensor = GripSensor("GS_001", "XYZ Robotics", robot_arm)

# Add sensors to the robot arm
robot_arm.add_joint_consumption_sensor(current_sensor)
robot_arm.add_grip_sensor(grip_sensor)
```
