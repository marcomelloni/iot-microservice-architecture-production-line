
from typing import Dict
import random
import json
from datetime import datetime 

class Joint:
    def __init__(self, joint_id: str):
        self.joint_id: str = joint_id
        self.consumption: float = 0.0
        self.timestamp: datetime = None

    def update_consumption(self):
        """Simula un aumento del consumo per il giunto"""
        self.consumption += random.uniform(0.1, 1.0)  # Aumenta il consumo in modo casuale
        self.timestamp = datetime.utcnow()

    def reset(self):
        """Ripristina il consumo del giunto"""
        self.consumption = 0.0
        self.timestamp = None

    def get_json(self) -> Dict:
        """Restituisce lo stato del giunto in formato JSON"""
        return {
            "joint_id": self.joint_id,
            "consumption": self.consumption,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
