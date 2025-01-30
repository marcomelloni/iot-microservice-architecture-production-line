from typing import Dict
from model.joint import Joint
from model.sensor import Sensor

class RobotArm:
    def __init__(self, arm_id: str):
        self.arm_id: str = arm_id
        self.joints: Dict[str, Joint] = {}  # Giunti del braccio robotico
        self.joint_consumptions_sensors: Dict[str, Sensor] = {}  # Sensori di consumo dei giunti
        self.grip_sensors: Dict[str, Sensor] = {}  # Sensori di presa

    def add_joint(self, joint: Joint):
        """Aggiungi un giunto al braccio robotico"""
        self.joints[joint.joint_id] = joint

    def add_joint_consumption_sensor(self, sensor: Sensor):
        """Aggiungi un sensore di consumo dei giunti al braccio robotico"""
        self.joint_consumptions_sensors[sensor.device_id] = sensor

    def add_grip_sensor(self, sensor: Sensor):
        """Aggiungi un sensore di presa al braccio robotico"""
        self.grip_sensors[sensor.device_id] = sensor

    def get_joint_consumption_sensors(self):
        """Restituisce i sensori di consumo dei giunti del braccio robotico"""
        return list(self.joint_consumptions_sensors.values())

    def get_grip_sensors(self):
        """Restituisce i sensori di presa del braccio robotico"""
        return list(self.grip_sensors.values())

    def reset(self):
        """Ripristina lo stato di tutti i giunti del braccio"""
        for joint in self.joints.values():
            joint.reset()

    def get_json_joint_consumptions(self) -> Dict:
        """Restituisce i consumi dei giunti in formato JSON"""
        return {
            "robot_arm_id": self.arm_id,
            "joint_consumption_sensors": [sensor.get_json_measurement() for sensor in self.joint_consumptions_sensors.values()]
        }
    
    def get_json_grip(self) -> Dict:
        """Restituisce lo stato di presa del braccio robotico in formato JSON"""
        return {
            "robot_arm_id": self.arm_id,
            "grip_sensors": [sensor.get_json_measurement() for sensor in self.grip_sensors.values()]
        }