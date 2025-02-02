from flask import request
from flask_restful import Resource
from dto.robot_arm_entity_response import RobotArmEntityResponse

class FaultActuatorResource(Resource):
    """Resource to manage the end effector weight for a specific robot arm"""

    def __init__(self, **kwargs):
        # Inject the DataManager instance
        self.data_manager = kwargs['data_manager']

    def get(self):
        """GET the end effector weight for a specific robot arm"""
        
        faults = self.data_manager.get_robots_fault()
        return faults, 200

    def post(self):
        """POST fault production line"""
        
        data = request.get_json()
        
        try:
            robot_id = data['robot_id']
            fault = data['fault']
            self.data_manager.set_robot_fault(robot_id, fault)
            return {"message": "Fault added successfully"}, 200
        except ValueError as e:
            return {"message": str(e)}, 400
