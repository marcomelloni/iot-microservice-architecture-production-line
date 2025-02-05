from model.robot_arm import RobotArm
from model.production_line import ProductionLine
import time

# Creazione dei robot
robot_arm_1 = RobotArm("RA_001", "XYZ Robotics", 3, 1)
robot_arm_2 = RobotArm("RA_002", "XYZ Robotics", 3, 1)
robot_arm_3 = RobotArm("RA_003", "XYZ Robotics", 3, 1)

# Creazione della linea di produzione (ma non attivata automaticamente)
production_line = ProductionLine("PL_001")

# Aggiunta dei robot alla linea di produzione
production_line.add_robot_arm(robot_arm_1)
production_line.add_robot_arm(robot_arm_2)
production_line.add_robot_arm(robot_arm_3)

# Avvio della produzione solo se il file viene eseguito direttamente
if __name__ == "__main__":
    production_line.activate()
    # Avvio del client MQTT
    production_line.start_mqtt_client()

    # Inizio del monitoraggio e pubblicazione dei dati dei sensori
    production_line.monitor_and_publish()
