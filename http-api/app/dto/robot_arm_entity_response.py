import json

class RobotArmEntityResponse:
    """ Location Entity Response DTO Class """
    def __init__(self, arm_id, manufacturer, number_of_joints):
        self.arm_id = arm_id
        self.manufacturer = manufacturer
        self.number_of_joints = number_of_joints

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
