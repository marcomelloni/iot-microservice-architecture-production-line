from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource
from dto.robot_arm_entity_response import RobotArmEntityResponse

class ProductionLineResource(Resource):
    """Resource to getall the robot arms in the production line"""

    def __init__(self, **kwargs):
        # Inject the DataManager instance
        self.data_manager = kwargs['data_manager']

    def get(self):
        """GET all robot arms in the production line"""
        
        result_robot_list = []
        
        # Itera attraverso tutti i robot nella lista
        for robot in self.data_manager.robot_arm_list:
            # Usa number_of_joints per ottenere il numero di giunti
            robot_entity_response = RobotArmEntityResponse(
                robot.arm_id,
                robot.manufacturer,
                robot.number_of_joints  
            )
            result_robot_list.append(robot_entity_response.__dict__)

        return result_robot_list, 200
