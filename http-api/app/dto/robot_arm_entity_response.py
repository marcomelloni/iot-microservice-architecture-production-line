import json


class RobotArmEntityResponse:
    """
    Represents the response entity for a robot arm's details.
    """

    def __init__(self, arm_id, manufacturer, number_of_joints):
        """
        Initializes the RobotArmEntityResponse with arm ID, manufacturer, and number of joints.

        :param arm_id: The unique identifier of the robot arm.
        :param manufacturer: The manufacturer of the robot arm.
        :param number_of_joints: The number of joints in the robot arm.
        """
        self.arm_id = arm_id
        self.manufacturer = manufacturer
        self.number_of_joints = number_of_joints

    def to_json(self):
        """
        Converts the RobotArmEntityResponse object to a JSON string.
        """
        return json.dumps(self, default=lambda o: o.__dict__)
