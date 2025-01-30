import threading
import time
from datetime import datetime
from typing import Dict
from model.sensor import Sensor
from model.robot_arm import RobotArm
from model.production_line import ProductionLine  # Import della linea di produzione

class CurrentSensor(Sensor):
    def __init__(self, device_id: str, device_manufacturer: str, robot_arm: 'RobotArm', production_line: 'ProductionLine'):
        super().__init__(device_id, "Current Sensor", device_manufacturer)
        self.robot_arm: RobotArm = robot_arm
        self.production_line: ProductionLine = production_line  # Riferimento alla linea di produzione
        self.running = False
        self._thread = threading.Thread(target=self._auto_update, daemon=True)

    def start_auto_update(self):
        """Avvia l'aggiornamento automatico delle misure se la linea è attiva"""
        if not self.running:
            self.running = True
            self._thread.start()

    def stop_auto_update(self):
        """Ferma l'aggiornamento automatico"""
        self.running = False

    def _auto_update(self):
        """Aggiorna i dati ogni secondo SOLO SE la linea di produzione è attiva"""
        while self.running:
            if self.production_line.active:  # Controlla lo stato della linea di produzione
                self.update_measurement()
            time.sleep(1)  # Aspetta 1 secondo

    def update_measurement(self):
        """Simula il consumo di ogni joint nel braccio robotico"""
        for joint in self.robot_arm.joints.values():
            joint.update_consumption()
        self.timestamp = datetime.utcnow()

    def reset(self):
        """Ripristina lo stato di tutti i giunti del braccio associato"""
        for joint in self.robot_arm.joints.values():
            joint.reset()

    def get_total_consumption(self) -> float:
        """Restituisce il consumo totale dei giunti del braccio robotico"""
        return sum(joint.consumption for joint in self.robot_arm.joints.values())

    def get_json_measurement(self) -> Dict:
        """Restituisce i dati del sensore in formato JSON"""
        return {
            "device_id": self.device_id,
            "total_consumption": self.get_total_consumption(),
            "joints": [joint.get_json() for joint in self.robot_arm.joints.values()]
        }
