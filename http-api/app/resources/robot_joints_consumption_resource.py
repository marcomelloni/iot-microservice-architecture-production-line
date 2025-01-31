from flask import request
from flask_restful import Resource
from dto.joint_entity_response import JointEntityResponse
from model.joints_model import JointsModel
from datetime import datetime

class RobotJointsConsumptionResource(Resource):
    """Resource to manage the consumption of joints for a specific robot arm"""

    def __init__(self, **kwargs):
        # Inject the DataManager instance
        self.data_manager = kwargs['data_manager']

    def get(self, robot_id):
        """GET the joint consumption data for a specific robot arm"""
        
        robot_arm = self.data_manager.get_robot_arm(robot_id)  # Changed here to use get_robot_arm
        if not robot_arm:
            return {"message": "Robot not found"}, 404
        
        # Collect joint data for the robot arm
        joint_data_list = []
        for joint_id, joint in robot_arm.joints.items():
            joint_entity_response = JointEntityResponse(joint.joint_id, joint.consumption, joint.timestamp)
            joint_data_list.append(joint_entity_response.__dict__)
        
        return joint_data_list, 200

    def post(self, robot_id):
        """POST new joint consumption data for a specific robot arm"""
        
        data = request.get_json()
        
        # Validation of the received data
        try:
            joint_id = data['joint_id']
            consumption = data['consumption']
            timestamp = data['timestamp']
            joint = JointsModel(joint_id, consumption, timestamp)
        except KeyError as e:
            return {"message": f"Missing key: {e}"}, 400
        except ValueError as e:
            return {"message": str(e)}, 400

        # Add the joint data to the DataManager
        robot_arm = self.data_manager.get_robot_arm(robot_id)  # Changed here to use get_robot_arm
        if not robot_arm:
            return {"message": "Robot not found"}, 404
        
        if joint.joint_id in robot_arm.joints:
            self.data_manager.update_joint_to_robot(robot_id, joint)
            return {"message": "Joint already exists, data updated successfully"}, 201
        else:
            self.data_manager.add_joint_to_robot(robot_id, joint) 
            return {"message": "Joint consumption data added successfully"}, 201
