from abc import ABC, abstractmethod
from datetime import datetime


class Sensor(ABC):
    def __init__(self, sensor_id, sensor_type, manufacturer):
        self.id = sensor_id
        self.type = sensor_type
        self.manufacturer = manufacturer
        self.value = self.measure()
        self.timestamp = datetime.now()

    def __str__(self):
        return f"Sensor(id={self.id}, type={self.type}, manufacturer={self.manufacturer}, timestamp={self.timestamp})"

    def __repr__(self):
        return str(self)

    @abstractmethod
    def measure(self):
        pass

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "manufacturer": self.manufacturer,
            "value": self.value,
            "timestamp": self.timestamp.isoformat()
        }
