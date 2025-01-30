import json


class JointConsumptionDTO:
    def __init__(self, uuid, joint_id, current_measurement, current_sensor):
        self.uuid = uuid
        self.joint_id = joint_id
        self.current_measurement = current_measurement
        self.current_sensor = current_sensor

    @staticmethod
    def from_creation_dto(joint_creation_request):
        return JointConsumptionDTO(
            joint_creation_request.joint_id,
            joint_creation_request.current_measurement,
            joint_creation_request.current_sensor
        )

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
