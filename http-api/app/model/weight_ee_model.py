import json


class WeightEndEffectorDTO:
    def __init__(self, uuid: int, robotic_arm_id: int, ee_id: int, weight: int):
        self.uuid = uuid
        self.robotic_arm_id = robotic_arm_id
        self.ee_id = ee_id
        self.weight = weight

    @staticmethod
    def from_creation_dto(weight_ee_creation_request):
        return WeightEndEffectorDTO(
            weight_ee_creation_request.uuid,
            weight_ee_creation_request.robotic_arm_id,
            weight_ee_creation_request.ee_id,
            weight_ee_creation_request.weight
        )

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
