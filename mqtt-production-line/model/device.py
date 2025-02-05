from typing import Dict


class Device:
    """
    Represents a generic device with an ID, type, and manufacturer.
    Provides methods to get a JSON representation of the device.
    """

    def __init__(self, device_id: str, device_type: str, device_manufacturer: str):
        """
        Initializes the device with an ID, type, and manufacturer.
        """
        self.device_id: str = device_id
        self.device_type: str = device_type
        self.device_manufacturer: str = device_manufacturer

    def get_json_description(self) -> Dict:
        """
        Returns a JSON representation of the device.
        """
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_manufacturer": self.device_manufacturer
        }

    def get_json_measurement(self):
        """
        This method must be implemented by subclasses.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")
