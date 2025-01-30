import threading
import time
from datetime import datetime
from typing import Dict
from model.sensor import Sensor
from model.robot_arm import RobotArm
import math  # Per utilizzare la funzione seno

class GripSensor(Sensor):
    def __init__(self, device_id: str, device_manufacturer: str, robot_arm: 'RobotArm'):
        super().__init__(device_id, "Grip Sensor", device_manufacturer)
        self.grip_force: float = 0.0  # Valore iniziale della forza di presa
        self.robot_arm: RobotArm = robot_arm
        self.timestamp: datetime = None
        self._stop_event = threading.Event()  # Evento di stop per il thread
        self._min_grip_force = 0.0  # Forza minima di presa
        self._max_grip_force = 10.0  # Forza massima di presa
        self._frequency = 0.1  # Frequenza della sinusoide (controlla la velocità del cambiamento)
        self._amplitude = (self._max_grip_force - self._min_grip_force) / 2  # Ampiezza della sinusoide

    def _auto_update(self):
        """Aggiorna automaticamente la forza di presa seguendo una funzione sinusoidale"""
        time_elapsed = 0  # Variabile per tracciare il tempo passato
        while not self._stop_event.is_set():
            # Funzione seno che varia tra -1 e 1
            # La forza di presa varia tra min e max in modo sinusoidale
            self.grip_force = self._min_grip_force + self._amplitude * (math.sin(self._frequency * time_elapsed) + 1)

            # Aggiorna il timestamp dell'ultima lettura
            self.timestamp = datetime.utcnow()

            # Attendi 1 secondo prima di aggiornare di nuovo
            time.sleep(1)
            time_elapsed += 1

    def start_auto_update(self):
        """Avvia il thread che aggiorna automaticamente la misura della forza di presa"""
        self._stop_event.clear()  # Inizializza l'evento di stop
        self._update_thread = threading.Thread(target=self._auto_update)
        self._update_thread.start()

    def stop_auto_update(self):
        """Ferma l'aggiornamento automatico della misura della forza di presa"""
        self._stop_event.set()  # Imposta l'evento di stop
        self._update_thread.join()  # Attende che il thread termini

    def get_json_measurement(self) -> Dict:
        """Restituisce i dati del sensore di presa in formato JSON"""
        return {
            "device_id": self.device_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "grip_force_newton": self.grip_force
        }
