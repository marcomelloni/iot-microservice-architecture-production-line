from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource
from dto.robot_arm_entity_response import RobotArmEntityResponse

class ProductionLineResource(Resource):
    """Resource to getall the robot arms in the production line"""

    def __init__(self, **kwargs):
        # Inject the DataManager instance
        self.data_manager = kwargs['data_manager']

    def get(self, device_id):
        """GET all robot arms in the production line"""
        result_robot_list = []
        for robot in self.data_manager.robot_arm_list.values():
            robot_entity_response =  RobotArmEntityResponse(robot.uuid,
                                                            robot.name,
                                                            robot.locationId,
                                                            robot.manufacturer,
                                                            robot.software_version,
                                                            robot.latitude,
                                                            robot.longitude,
                                                            robot.arm_length)
            result_robot_list.append(robot_entity_response.__dict__)
        return result_robot_list, 200

    def post(self, device_id):
       return '', 501

