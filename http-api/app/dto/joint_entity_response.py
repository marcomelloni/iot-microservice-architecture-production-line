class JointEntityResponse:
    """
    Represents the response entity for a joint's telemetry data.
    """

    def __init__(self, joint_id, consumption, timestamp):
        """
        Initializes the JointEntityResponse with joint ID, consumption, and timestamp.

        :param joint_id: The unique identifier of the joint.
        :param consumption: The consumption value of the joint.
        :param timestamp: The timestamp of the measurement.
        """
        self.joint_id = joint_id
        self.consumption = consumption
        self.timestamp = timestamp
