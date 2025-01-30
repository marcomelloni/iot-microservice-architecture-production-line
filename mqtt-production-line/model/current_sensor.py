import random

from sensor import Sensor


class CurrentSensor(Sensor):
    def __init__(self, sensor_id, manufacturer):
        super().__init__(sensor_id, "current", manufacturer)

    def measure(self):
        return random.randint(0, 100)
