import json

class RobotArmEntityResponse:
    """ Robot Arm Entity Response DTO Class """
    def __init__(self, uuid, name, latitude, longitude, device_list):
        self.uuid = uuid
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.device_list = device_list

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)