import json
from datetime import datetime


class JointsModel:
    """
    JointsModel represents an individual joint in a robotic arm, including
    its power consumption and a timestamp for data tracking.
    """

    def __init__(self, joint_id: str, consumption: float, timestamp: str):
        """
        Initializes a Joint instance with an identifier, power consumption, and timestamp.

        :param joint_id: Unique identifier for the joint.
        :param consumption: Power consumption in watts.
        :param timestamp: Timestamp indicating the last measurement.
        """
        self.timestamp = timestamp
        self.consumption = consumption
        self.joint_id: str = joint_id
        self.set_consumption(consumption)
        self.set_timestamp(timestamp)

    def set_consumption(self, consumption: float):
        """
        Sets the power consumption value.

        :param consumption: Power consumption in watts.
        :raises ValueError: If the provided consumption value is negative.
        """
        if consumption < 0:
            raise ValueError("Power consumption cannot be negative.")
        self.consumption = consumption

    def set_timestamp(self, timestamp: str):
        """
        Validates and sets the timestamp.

        :param timestamp: Timestamp in ISO 8601 format (e.g., "2024-01-31T12:00:00").
        :raises ValueError: If the timestamp format is incorrect.
        """
        try:
            datetime.fromisoformat(timestamp)  # Ensure valid ISO 8601 format
            self.timestamp = timestamp
        except ValueError:
            raise ValueError("Invalid timestamp format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS).")

    def to_json(self) -> str:
        """
        Serializes the JointsModel object to a JSON string.
        :return: JSON representation of the JointsModel instance.
        """
        return json.dumps(self, default=lambda o: o.__dict__)
