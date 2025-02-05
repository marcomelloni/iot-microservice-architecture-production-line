from datetime import datetime
from typing import Dict
from .sensor import Sensor
import math


class GripSensor(Sensor):
    """
    Represents a grip sensor that measures the grip force of a robot arm.
    Simulates grip force using a sine wave.
    """

    def __init__(self, device_id: str, device_manufacturer: str):
        """
        Initializes the grip sensor with a sine wave for simulating grip force.
        """
        self.timestamp = datetime.now()
        self.value = 0.0

        super().__init__(device_id, device_manufacturer, self.value, "A", self.timestamp)
        self.running = False

        self._min_grip_force = 0.0  # Minimum grip force
        self._max_grip_force = 10.0  # Maximum grip force
        self._frequency = 0.1  # Frequency of the sine wave (controls the speed of change)
        self._amplitude = (self._max_grip_force - self._min_grip_force) / 2  # Amplitude of the sine wave

    def start_auto_update(self):
        """
        Starts the automatic update of the grip force if the line is active.
        """
        self.update_consumption()

    def update_consumption(self):
        """
        Updates the grip force based on a sine wave.
        """
        self.value = self._min_grip_force + self._amplitude * (math.sin(self._frequency) + 1)
        self.timestamp = datetime.now()

    def get_json_measurement(self) -> Dict:
        """
        Returns the grip sensor data in JSON format.
        """
        return super().get_json_measurement()
