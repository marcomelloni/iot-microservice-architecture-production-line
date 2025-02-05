from flask import request
from flask_restful import Resource


class FaultActuatorResource(Resource):
    """
    Resource to manage the faults for a specific robot arm.
    Provides endpoints to get and set faults.
    """

    def __init__(self, **kwargs):
        """
        Initializes the FaultActuatorResource with a DataManager instance.

        :param kwargs: Keyword arguments containing the DataManager instance.
        """
        self.data_manager = kwargs['data_manager']

    def get(self):
        """
        GET the faults for all robot arms.

        :return: A dictionary of robot IDs and their corresponding faults.
        """
        faults = self.data_manager.get_robots_fault()
        return faults, 200

    def post(self):
        """
        POST a new fault for a specific robot arm.

        Expects a JSON payload with 'robot_id' and 'fault'.

        :return: A success message if the fault is added successfully, otherwise an error message.
        """
        data = request.get_json()

        try:
            robot_id = data['robot_id']
            fault = data['fault']
            self.data_manager.set_robot_fault(robot_id, fault)
            return {"message": "Fault added successfully"}, 200
        except ValueError as e:
            return {"message": str(e)}, 400
