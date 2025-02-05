from typing import Dict
from .current_sensor import CurrentSensor

class Joint:
    def __init__(self, joint_id: str):
        self.joint_id: str = joint_id
        self.current_sensor = CurrentSensor(joint_id, "ABB")

    def get_json(self) -> Dict:
        """Returns the joint status data in JSON format"""
        return {
            "joint_id": self.joint_id,
            "current_sensor": self.current_sensor.get_json_measurement()
        }
