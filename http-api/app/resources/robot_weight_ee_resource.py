from flask import request
from flask_restful import Resource


class RobotWeightEEResource(Resource):
    """
    Resource to manage the end effector weight for a specific robot arm.
    Provides endpoints to get and set the end effector weight.
    """

    def __init__(self, **kwargs):
        """
        Initializes the RobotWeightEEResource with a DataManager instance.

        :param kwargs: Keyword arguments containing the DataManager instance.
        """
        self.data_manager = kwargs['data_manager']

    def get(self, robot_id):
        """
        GET the end effector weight for a specific robot arm.

        :param robot_id: The ID of the robot arm.
        :return: A dictionary with the robot arm ID and its end effector weight.
        """
        robot_arm = self.data_manager.get_robot_arm(robot_id)
        if not robot_arm:
            return {"message": "Robot not found"}, 404

        return {"arm_id": robot_arm.arm_id, "weight_ee": robot_arm.weight_ee}, 200

    def post(self, robot_id):
        """
        POST new end effector weight for a specific robot arm.

        Expects a JSON payload with 'weight_ee'.

        :param robot_id: The ID of the robot arm.
        :return: A success message if the weight is updated successfully, otherwise an error message.
        """
        data = request.get_json()

        try:
            weight_ee = data['weight_ee']
            robot_arm = self.data_manager.get_robot_arm(robot_id)
            if not robot_arm:
                return {"message": "Robot not found"}, 404

            robot_arm.set_end_effector_weight(weight_ee)
            return {"message": "End effector weight updated successfully"}, 200
        except KeyError:
            return {"message": "Missing 'weight_ee' data"}, 400
        except ValueError as e:
            return {"message": str(e)}, 400
