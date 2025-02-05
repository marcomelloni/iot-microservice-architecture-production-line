from typing import Dict, List
from .joint import Joint
from .grip_sensor import GripSensor


class RobotArm:
    """
    Represents a robot arm with multiple joints and grip sensors.
    Manages the activation, deactivation, and monitoring of the joints and grip sensors.
    """

    def __init__(self, arm_id: str, manufacturer: str, n_joints: int, n_grips: int):
        """
        Initializes the robot arm with an ID, manufacturer, number of joints, and number of grip sensors.
        """
        self.arm_id: str = arm_id
        self.manufacturer: str = manufacturer
        self.joints: List[Joint] = [Joint(f"joint_{i}") for i in range(n_joints)]  # Joints of the robot arm
        self.grips: List[GripSensor] = [GripSensor(f"grip_{i}", "ABB") for i in
                                        range(n_grips)]  # Grip sensors of the robot arm
        self.idle = True

    def start(self):
        """Starts the robot arm"""
        self.idle = False
        self.start_auto_update()

    def stop(self):
        """Stops the robot arm"""
        self.idle = True
        print(f"Robot arm {self.arm_id} stopped.")

    def add_joint(self, joint: Joint):
        """Adds a joint to the robot arm"""
        self.joints.append(joint)

    def add_grip_sensor(self, grip_sensor: GripSensor):
        """Adds a grip sensor to the robot arm"""
        self.grips.append(grip_sensor)

    def get_grip_sensors(self):
        """Returns the grip sensors of the robot arm"""
        return self.grips

    def reset(self):
        """Resets the state of all joints of the arm"""
        for i, joint in enumerate(self.joints):
            joint.current_sensor.reset()
            print(f"Reset joint_{i} with value {joint.current_sensor.value}")

    def get_json_consumptions(self) -> Dict:
        """Returns the joint consumptions in JSON format"""
        return {
            "robot_arm_id": self.arm_id,
            "joint_consumption_sensors": [joint.get_json() for joint in self.joints]
        }

    def get_json_grip(self) -> Dict:
        """Returns the grip state of the robot arm in JSON format"""
        return {
            "robot_arm_id": self.arm_id,
            "grip_sensors": [grip.get_json_measurement() for grip in self.grips]
        }

    def start_auto_update(self):
        """Starts automatic updates of the sensors"""
        for grip_sensor in self.grips:
            grip_sensor.start_auto_update()

        for joint in self.joints:
            joint.current_sensor.start_auto_update()
