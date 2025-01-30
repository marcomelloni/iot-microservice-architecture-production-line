import json


class JointConsumptionsUpdateRequest:
    def __init__(self, uuid:int, robotic_arm_id:int, joint_ids:list, joint_updates:list):
        self.uuid = uuid
        self.robotic_arm_id = robotic_arm_id
        self.joint_ids = joint_ids
        self.joint_updates = joint_updates

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
