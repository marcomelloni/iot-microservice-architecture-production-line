from typing import Dict
import json

class Device:
    def __init__(self, device_id: str, device_type: str, device_manufacturer: str):
        self.device_id: str = device_id
        self.device_type: str = device_type
        self.device_manufacturer: str = device_manufacturer

    def get_json_description(self) -> Dict:
        """Restituisce una rappresentazione JSON del dispositivo"""
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer
        }

    def get_json_measurement(self):
        raise NotImplementedError("Questo metodo deve essere implementato dalle sottoclassi.")
