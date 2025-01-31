from model.joint_model import JointConsumptionDTO
from model.weight_ee_model import WeightEndEffectorDTO
from model.robot_arm_model import RobotArmModel
class DataManager:
    """DataManager class to manage the robot arms of the production line and their data"""
    
    robot_arm_list = []
    joint_dictionary = {}
    weight_end_effector_dictionary = {}

    # ROBOT ARM MANAGEMENT
    def add_robot_arm(self, new_robot_arm):
        # Check the correct instance for the variable new_robot_arm
        if isinstance(new_robot_arm, RobotArmModel):
            self.robot_arm_list.append(new_robot_arm)
        else:
            raise TypeError("Error adding new Robot Arm ! Only RobotArmDTO are allowed !")

    def add_joint(self, new_joint):
        # Check the correct instance for the variable new_joint
        if isinstance(new_joint, JointConsumptionDTO):
            self.joint_dictionary[new_joint.uuid] = new_joint
        else:
            raise TypeError("Error adding new Joint ! Only JointModel are allowed !")

    def update_joint(self, updated_joint):
        # Check the correct instance for the variable updated_joint
        if isinstance(updated_joint, JointConsumptionDTO):
            self.joint_dictionary[updated_joint.uuid] = updated_joint
        else:
            raise TypeError("Error updating the Joint ! Only JointModel are allowed !")

    def remove_joint(self, joint_uuid):
        if joint_uuid in self.joint_dictionary.keys():
            del self.joint_dictionary[joint_uuid]

    # WEIGHT END EFFECTOR MANAGEMENT
    def add_weight_end_effector(self, new_weight_end_effector):
        # Check the correct instance for the variable new_weight_end_effector
        if isinstance(new_weight_end_effector, WeightEndEffectorDTO):
            self.weight_end_effector_dictionary[new_weight_end_effector.uuid] = new_weight_end_effector
        else:
            raise TypeError("Error adding new Weight End Effector ! Only WeightEndEffectorDTO are allowed !")

    def update_weight_end_effector(self, updated_weight_end_effector):
        # Check the correct instance for the variable updated_weight_end_effector
        if isinstance(updated_weight_end_effector, WeightEndEffectorDTO):
            self.weight_end_effector_dictionary[updated_weight_end_effector.uuid] = updated_weight_end_effector
        else:
            raise TypeError("Error updating the Weight End Effector ! Only WeightEndEffectorDTO are allowed !")

    def remove_weight_end_effector(self, weight_end_effector_uuid):
        if weight_end_effector_uuid in self.weight_end_effector_dictionary.keys():
            del self.weight_end_effector_dictionary[weight_end_effector_uuid]
    """
    DataManager class is responsible for managing the data of the application.
    Abstracts the data storage and retrieval operations.
    In this implementation everything is stored in memory.
    """
