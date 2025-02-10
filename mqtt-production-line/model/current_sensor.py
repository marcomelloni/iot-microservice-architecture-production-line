import random
import threading

from datetime import datetime
from typing import Dict
from .sensor import Sensor


class CurrentSensor(Sensor):
    """
    Represents a current sensor that measures the electrical current consumption of a joint.
    Provides functionality to automatically update the measurement at regular intervals.
    """

    def __init__(self, device_id: str, device_manufacturer: str):
        self.timestamp = datetime.now()
        self.value = random.randint(85, 95)
        super().__init__(device_id, device_manufacturer, self.value, "A", self.timestamp)
        self.running = False
        # Thread for auto-update
        self._thread = None

    def update_consumption(self):
        """Simulates a very small increase in consumption for the joint"""
        self.value += random.uniform(0.00001, 0.000001)  # Increases consumption randomly
        self.timestamp = datetime.now()

    def start_auto_update(self):
        """Starts automatic measurement updates every second"""
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._auto_update)
            self._thread.start()

    def _auto_update(self):
        """Periodically updates consumption every second"""
        while self.running:
            self.update_consumption()

    def stop_auto_update(self):
        """Stops automatic updates"""
        self.running = False
        if self._thread is not None and self._thread.is_alive():
            self._thread.join()

    def reset(self):
        """Resets the joint's consumption"""
        self.value = 95.0
        self.timestamp = datetime.now()

    def get_json_measurement(self) -> Dict:
        """Returns the sensor data in JSON format"""
        return super().get_json_measurement()


"""{'robot_arm_id': 'RA_001', 'joint_consumption_sensors': [
    {'joint_id': 'joint_0', 'current_sensor': {'device_id': 'joint_0', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 107.26375397661127, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.150562'}},
    {'joint_id': 'joint_1', 'current_sensor': {'device_id': 'joint_1', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 87.48555998110078, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.090694'}},
    {'joint_id': 'joint_2', 'current_sensor': {'device_id': 'joint_2', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 87.20065898182008, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.138400'}}]}


{'robot_arm_id': 'RA_002', 'joint_consumption_sensors': [
    {'joint_id': 'joint_0', 'current_sensor': {'device_id': 'joint_0', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 107.04546797716239, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.216551'}},
    {'joint_id': 'joint_1', 'current_sensor': {'device_id': 'joint_1', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 87.04775198220614, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.175623'}},
    {'joint_id': 'joint_2', 'current_sensor': {'device_id': 'joint_2', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 86.95486998244064, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.156829'}}]}


{'robot_arm_id': 'RA_003', 'joint_consumption_sensors': [{
    'joint_id': 'joint_0', 'current_sensor': {'device_id': 'joint_0', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 107.26763597660147, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.548974'}},
                                                         {'joint_id': 'joint_1', 'current_sensor': {'device_id': 'joint_1', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 87.1943939818359, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.555250'}},
                                                         {'joint_id': 'joint_2', 'current_sensor': {'device_id': 'joint_2', 'device_type': 'Sensor', 'device_manufacturer': 'ABB', 'value': 87.15930998192448, 'unit': 'A', 'timestamp': '2025-02-05T11:37:43.513594'}}]}"""
