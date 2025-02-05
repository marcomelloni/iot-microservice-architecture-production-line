from typing import Dict
from .joints_model import JointsModel
import json


class RobotArmModel:
    """
    RobotArmModel represents a robotic arm with configurable properties,
    including manufacturer details, joint configurations, and payload capacity.
    """

    def __init__(self, arm_id: str, manufacturer: str):
        """
        Initializes a Robot Arm instance with a unique identifier and manufacturer details.

        :param arm_id: Unique identifier for the robotic arm.
        :param manufacturer: Name of the company that manufactured the robotic arm.
        """
        self.arm_id: str = arm_id
        self.manufacturer: str = manufacturer
        self.joints: Dict[str, JointsModel] = {}  # Dictionary to store joint configurations
        self.weight_ee: float = 0.0  # Weight of the end effector (EE) in kg

    def add_joint(self, joint_id: str, joint_model: JointsModel):
        """
        Adds or updates a joint configuration in the robot arm.

        :param joint_id: Name of the joint (e.g., 'shoulder', 'elbow').
        :param joint_model: Joint-specific data, such as position, torque, or speed.
        """
        self.joints[joint_id] = joint_model

    def set_end_effector_weight(self, weight: float):
        """
        Sets the weight of the end effector.

        :param weight: Weight in kilograms.
        :raises ValueError: If the provided weight is negative.
        """
        if weight < 0:
            raise ValueError("End effector weight cannot be negative.")
        self.weight_ee = weight

    @property
    def number_of_joints(self):
        """
        Returns the number of joints present in the robot arm.

        :return: The number of joints.
        """
        return len(self.joints)

    def to_json(self):
        """
        Serializes the RobotArmModel object to a JSON string.

        :return: JSON representation of the RobotArmModel instance.
        """
        return json.dumps(self, default=lambda o: o.__dict__)
