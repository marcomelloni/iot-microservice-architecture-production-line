from current_sensor import CurrentSensor


class Joint:
    def __init__(self, joint_id):
        self.id = joint_id
        self.current_sensor = CurrentSensor(joint_id, "Acme Inc.")

    def serialize(self):
        return {
            "id": self.id,
            "current_sensor": self.current_sensor.serialize(),
        }
