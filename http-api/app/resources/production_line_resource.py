from flask_restful import Resource
from ..dto.robot_arm_entity_response import RobotArmEntityResponse


class ProductionLineResource(Resource):
    """
    Resource to get all the robot arms in the production line.
    Provides an endpoint to retrieve the list of robot arms.
    """

    def __init__(self, **kwargs):
        """
        Initializes the ProductionLineResource with a DataManager instance.

        :param kwargs: Keyword arguments containing the DataManager instance.
        """
        self.data_manager = kwargs['data_manager']

    def get(self):
        """
        GET all robot arms in the production line.

        Iterates through all robot arms in the data manager's list,
        creates a response entity for each robot arm, and returns the list.

        :return: A list of dictionaries representing the robot arms.
        """
        result_robot_list = []

        # Iterate through all robots in the list
        for robot in self.data_manager.robot_arm_list:
            # Use number_of_joints to get the number of joints
            robot_entity_response = RobotArmEntityResponse(
                robot.arm_id,
                robot.manufacturer,
                robot.number_of_joints
            )
            result_robot_list.append(robot_entity_response.__dict__)

        return result_robot_list, 200
