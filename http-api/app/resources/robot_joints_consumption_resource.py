from flask import request
from flask_restful import Resource
from ..dto.joint_entity_response import JointEntityResponse
from ..model.joints_model import JointsModel
from ..model.robot_arm_model import RobotArmModel


class RobotJointsConsumptionResource(Resource):
    """
    Resource to manage the consumption of joints for a specific robot arm.
    Provides endpoints to get and set joint consumption data.
    """

    def __init__(self, **kwargs):
        """
        Initializes the RobotJointsConsumptionResource with a DataManager instance.

        :param kwargs: Keyword arguments containing the DataManager instance.
        """
        self.data_manager = kwargs['data_manager']

    def get(self, robot_id):
        """
        GET the joint consumption data for a specific robot arm.

        :param robot_id: The ID of the robot arm.
        :return: A list of dictionaries representing the joint consumption data.
        """
        robot_arm = self.data_manager.get_robot_arm(robot_id)
        if not robot_arm:
            return {"message": "Robot not found"}, 404

        # Collect joint data for the robot arm
        joint_data_list = []
        for joint_id, joint in robot_arm.joints.items():
            joint_entity_response = JointEntityResponse(joint.joint_id, joint.consumption, joint.timestamp)
            joint_data_list.append(joint_entity_response.__dict__)

        return joint_data_list, 200

    def post(self, robot_id):
        """
        POST multiple joint consumption data for a specific robot arm.

        Expects a JSON payload with a list of joints, each containing 'joint_id', 'consumption', and 'timestamp'.

        :param robot_id: The ID of the robot arm.
        :return: A success message if the data is processed successfully, otherwise an error message.
        """
        data = request.get_json()

        # Check if the request contains the joint data
        try:
            joints_data = data['joints']
        except KeyError as e:
            return {"message": f"Missing key: {e}"}, 400
        except ValueError as e:
            return {"message": str(e)}, 400

        # Get the robot arm data
        robot_arm = self.data_manager.get_robot_arm(robot_id)
        if not robot_arm:
            # Setup a new default RobotArmModel
            robot_arm = RobotArmModel(arm_id=robot_id, manufacturer="DefaultManufacturer")
            self.data_manager.add_robot_arm(robot_arm)

        # Process each joint in the list
        for joint_data in joints_data:
            try:
                joint_id = joint_data['joint_id']
                consumption = joint_data['consumption']
                timestamp = joint_data['timestamp']
                joint = JointsModel(joint_id, consumption, timestamp)
            except KeyError as e:
                return {"message": f"Missing key: {e}"}, 400
            except ValueError as e:
                return {"message": str(e)}, 400

            # Add the joint to the robot arm
            self.data_manager.add_joint_to_robot(robot_id, joint)

        return {"message": "Joint consumption data processed successfully"}, 201
