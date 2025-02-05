import datetime
from .device import Device


class Sensor(Device):
    """
    Represents a generic sensor device.
    Provides methods to update and retrieve sensor measurements in JSON format.
    """

    def __init__(self, device_id: str, device_manufacturer: str, value: float, unit: str, timestamp: datetime):
        """
        Initializes the sensor with a value, unit, and timestamp.
        """
        super().__init__(device_id, "Sensor", device_manufacturer)
        self.value = value
        self.unit = unit
        self.timestamp = timestamp

    def update_measurement(self):
        """
        Updates the sensor measurement.
        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Not implemented method. It must be implemented in the subclasses")

    def get_json_measurement(self):
        """
        Returns the sensor data in JSON format.
        """
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
