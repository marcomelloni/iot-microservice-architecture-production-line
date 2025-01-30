
from model.device import Device

class Sensor(Device):
    def __init__(self, device_id: str, device_type: str, device_manufacturer: str):
        super().__init__(device_id, device_type, device_manufacturer)
        self.value = None
        self.unit = None
        self.timestamp = None  # Aggiunto timestamp

    def update_measurement(self):
        raise NotImplementedError("Questo metodo deve essere implementato dalle sottoclassi.")
