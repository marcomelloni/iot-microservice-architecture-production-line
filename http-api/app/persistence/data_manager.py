from ..model.robot_arm_model import RobotArmModel
from ..model.joints_model import JointsModel


class DataManager:
    """DataManager class to manage the robot arms of the production line and their data"""

    def __init__(self):
        """Initialize DataManager with empty data structures"""
        self.robot_arm_list = []  # List to store all robot arms
        self.joint_dictionary = {}  # Dictionary to store all joints by UUID
        self.weight_end_effector_dictionary = {}  # Dictionary to store end effector weight by robot ID
        self.fault_dictionary = {}  # Dictionary to store faults by robot ID

    # ROBOT ARM MANAGEMENT

    def add_robot_arm(self, new_robot_arm: RobotArmModel):
        """
        Adds a new robot arm to the robot_arm_list.

        :param new_robot_arm: The new robot arm object to be added.
        :raises TypeError: If the object is not an instance of RobotArmModel.
        """
        if isinstance(new_robot_arm, RobotArmModel):
            self.robot_arm_list.append(new_robot_arm)
        else:
            raise TypeError("Error adding new Robot Arm! Only RobotArmModel are allowed!")

    def get_robot_arm(self, arm_id: str) -> RobotArmModel:
        """
        Retrieves a robot arm by its ID.

        :param arm_id: The ID of the robot arm.
        :return: The robot arm object if found.
        :raises KeyError: If no robot arm with the given ID exists.
        """
        for robot in self.robot_arm_list:
            if robot.arm_id == arm_id:
                return robot
        return None

    def get_all_robot_arms(self) -> list:
        """
        Retrieves all robot arms.

        :return: List of all robot arm objects.
        """
        return self.robot_arm_list

    # JOINT MANAGEMENT

    def add_joint_to_robot(self, arm_id: str, new_joint: JointsModel):
        """
        Adds a new joint to a specific robot arm by associating it with the robot's arm.

        :param arm_id: The ID of the robot arm to which the joint should be added.
        :param new_joint: The new joint object to be added.
        :raises TypeError: If the object is not an instance of JointsModel.
        :raises KeyError: If no robot arm with the given ID exists.
        """
        if isinstance(new_joint, JointsModel):
            robot = self.get_robot_arm(arm_id)  # Get the robot arm by ID
            robot.add_joint(new_joint.joint_id, new_joint)  # Add joint to the robot arm
        else:
            raise TypeError("Error adding new Joint! Only JointsModel are allowed!")

    def get_joints_for_robot(self, arm_id: str) -> list:
        """
        Retrieves all joints associated with a specific robot arm.

        :param arm_id: The ID of the robot arm.
        :return: List of joint objects associated with the robot arm.
        :raises KeyError: If no robot arm with the given ID exists.
        """
        robot = self.get_robot_arm(arm_id)
        return list(robot.joints.values())  # Return all joints associated with this robot arm

    # WEIGHT END EFFECTOR MANAGEMENT

    def set_end_effector_weight(self, arm_id: str, weight: float):
        """
        Sets the end effector weight for a specific robot arm.

        :param arm_id: The ID of the robot arm.
        :param weight: The weight of the end effector in kilograms.
        :raises ValueError: If the weight is negative.
        :raises KeyError: If no robot arm with the given ID exists.
        """
        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        robot = self.get_robot_arm(arm_id)
        robot.set_end_effector_weight(weight)

        # Store the weight in the dictionary
        self.weight_end_effector_dictionary[arm_id] = weight

    def get_end_effector_weight(self, arm_id: str) -> float:
        """
        Retrieves the end effector weight for a specific robot arm.

        :param arm_id: The ID of the robot arm.
        :return: The weight of the end effector.
        :raises KeyError: If no weight is set for the robot arm.
        """
        if arm_id in self.weight_end_effector_dictionary:
            return self.weight_end_effector_dictionary[arm_id]
        raise KeyError(f"No end effector weight set for robot arm with ID {arm_id}.")

    # FAULT MANAGEMENT

    def set_robot_fault(self, arm_id: str, fault: str):
        """
        Sets a fault for a specific robot arm.

        :param arm_id: The ID of the robot arm.
        :param fault: The fault description.
        :raises KeyError: If no robot arm with the given ID exists.
        """
        # Store the fault in the dictionary
        self.fault_dictionary[arm_id] = fault

    def get_robots_fault(self):
        """
        Retrieves all faults.

        :return: Dictionary of robot ID and fault description.
        """
        return self.fault_dictionary
