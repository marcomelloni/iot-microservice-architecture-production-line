import json


class WeightEEUpdateRequest:
    def __init__(self, uuid:int, robotic_arm_id:int, ee_id:int, weight:int):
        self.uuid = uuid
        self.robotic_arm_id = robotic_arm_id
        self.ee_id = ee_id
        self.weight = weight

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)