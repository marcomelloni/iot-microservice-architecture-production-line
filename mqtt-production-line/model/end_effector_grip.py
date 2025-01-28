from grip_sensor import GripSensor


class EndEffectorGrip:
    def __init__(self, ee_grip_id):
        self.id = ee_grip_id
        self.grip_sensor = GripSensor(ee_grip_id, "Acme Inc.")

    def serialize(self):
        return {
            "id": self.id,
            "grip_sensor": self.grip_sensor.serialize(),
        }
