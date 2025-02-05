import time
import paho.mqtt.client as mqtt
from model.robot_arm import RobotArm
from model.production_line import ProductionLine
import threading

# Crea i robot arms
robot_arm_1 = RobotArm("RA_001", "XYZ Robotics", 3, 1)
robot_arm_2 = RobotArm("RA_002", "XYZ Robotics", 3, 1)
robot_arm_3 = RobotArm("RA_003", "XYZ Robotics", 3, 1)

# Crea la linea di produzione
production_line = ProductionLine("PL_001")

# Aggiungi i robot arms alla linea di produzione
production_line.add_robot_arm(robot_arm_1)
production_line.add_robot_arm(robot_arm_2)
production_line.add_robot_arm(robot_arm_3)

# Flag per il monitoraggio
monitoring_active = False

# Funzione di attivazione della linea di produzione
def activate_production_line():
    """Funzione per attivare la linea di produzione."""
    global monitoring_active
    production_line.activate()  # Riattiva la linea di produzione
    print("Linea di produzione attivata.")
    time.sleep(5)
    
    monitoring_active = True  # Abilita il monitoraggio
    start_monitoring_thread()  # Avvia il thread di monitoraggio

def deactivate_production_line():
    """Funzione per disattivare la linea di produzione."""
    global monitoring_active
    production_line.deactivate()  # Disattiva la linea di produzione
    monitoring_active = False  # Ferma il monitoraggio
    production_line.stop_monitor_and_publish()  # Ferma la pubblicazione dei dati
    print("Linea di produzione fermata.")

# Funzione per avviare il client MQTT e la pubblicazione dei dati
def start_mqtt_client():
    """Funzione per avviare il client MQTT e la pubblicazione dei dati."""
    production_line.start_mqtt_client()  # Avvia il client MQTT
    # Monitoraggio della produzione e pubblicazione dei dati
    production_line.monitor_and_publish()  # Avvia la pubblicazione dei dati

# Funzione principale per gestire la simulazione
def start_production_simulation():
    """Funzione principale per gestire la simulazione della produzione."""
    # Attiviamo la linea di produzione
    activate_production_line()

    # Avviamo il client MQTT e iniziamo la pubblicazione dei dati
    start_mqtt_client()

# Funzione per eseguire il monitoraggio in un thread separato
def start_monitoring_thread():
    """Avvia il thread per il monitoraggio della produzione."""
    def monitor():
        while monitoring_active:  # Esegui finché il monitoraggio è attivo
            production_line.monitor_and_publish()  # Pubblica i dati di monitoraggio
            time.sleep(3)  # Aggiungi un ritardo per evitare un ciclo troppo veloce

    # Avvia il thread per il monitoraggio
    monitoring_thread = threading.Thread(target=monitor)
    monitoring_thread.daemon = True  # Il thread termina quando il programma principale termina
    monitoring_thread.start()

# Avvia la simulazione della produzione
if __name__ == "__main__":
    start_production_simulation()

    # Fai partire un ciclo infinito per simulare la continua esecuzione
    while True:
        time.sleep(1)  # Mantieni il thread principale attivo
