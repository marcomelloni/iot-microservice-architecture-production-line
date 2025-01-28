class RoboticArm:
    def __init__(self, arm_id, manufacturer):
        self.arm_id = arm_id
        self.manufacturer = manufacturer
        self._state = "idle"
        self.joints = []
        self.end_effector_grip = None

    def add_joints(self, joints):
        self.joints = joints

    def add_end_effector_grip(self, end_effector_grip):
        self.end_effector_grip = end_effector_grip

    def serialize(self):
        return {
            "arm_id": self.arm_id,
            "manufacturer": self.manufacturer,
            "state": self._state,
            "joints": [joint.serialize() for joint in self.joints],
            "end_effector_grip": self.end_effector_grip.serialize() if self.end_effector_grip else None
        }
