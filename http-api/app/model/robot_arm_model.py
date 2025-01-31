import json

class RobotArmModel:
    """ Robot Arm Model Class describing the robot arm properties """

    def __init__(self, uuid, name, location_id, manufacturer, software_version, latitude, longitude, arm_length, max_payload, degrees_of_freedom):
        """ Initialize the Robot Arm with the provided properties """
        self.uuid = uuid
        self.name = name
        self.locationId = location_id
        self.type = "device.actuator"
        self.manufacturer = manufacturer
        self.software_version = software_version
        self.latitude = latitude
        self.longitude = longitude
        self.arm_length = arm_length
        self.max_payload = max_payload
        self.degrees_of_freedom = degrees_of_freedom

    def to_json(self):
        """ Serialize the Robot Arm to a JSON string """
        return json.dumps(self, default=lambda o: o.__dict__)
