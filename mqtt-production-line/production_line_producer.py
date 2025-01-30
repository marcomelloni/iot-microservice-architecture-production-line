from model.production_line import ProductionLine
from model.robot_arm import RobotArm
from model.joint import Joint
from model.current_sensor import CurrentSensor
from model.grip_sensor import GripSensor
import time

# Create joints and the first robot arm
joint_1 = Joint("J1")
joint_2 = Joint("J2")
joint_3 = Joint("J3")
robot_arm_1 = RobotArm("RA_001")
robot_arm_1.add_joint(joint_1)
robot_arm_1.add_joint(joint_2)
robot_arm_1.add_joint(joint_3)

# Create joints and the second robot arm
joint_1_2 = Joint("J1")
joint_2_2 = Joint("J2")
joint_3_2 = Joint("J3")
robot_arm_2 = RobotArm("RA_002")
robot_arm_2.add_joint(joint_1_2)
robot_arm_2.add_joint(joint_2_2)
robot_arm_2.add_joint(joint_3_2)

# Create joints and the third robot arm
joint_1_3 = Joint("J1")
joint_2_3 = Joint("J2")
joint_3_3 = Joint("J3")
robot_arm_3 = RobotArm("RA_003")
robot_arm_3.add_joint(joint_1_3)
robot_arm_3.add_joint(joint_2_3)
robot_arm_3.add_joint(joint_3_3)

# Create the production line
production_line = ProductionLine("PL_001")

# Add the robot arms to the production line
production_line.add_robot_arm(robot_arm_1)
production_line.add_robot_arm(robot_arm_2)
production_line.add_robot_arm(robot_arm_3)

# Create the sensors for the first robot arm
current_sensor_1 = CurrentSensor("CS_001", "XYZ Robotics", robot_arm_1, production_line)
grip_sensor_1 = GripSensor("GS_001", "XYZ Robotics", robot_arm_1)

# Create the sensors for the second robot arm
current_sensor_2 = CurrentSensor("CS_002", "XYZ Robotics", robot_arm_2, production_line)
grip_sensor_2 = GripSensor("GS_002", "XYZ Robotics", robot_arm_2)

# Create the sensors for the third robot arm
current_sensor_3 = CurrentSensor("CS_003", "XYZ Robotics", robot_arm_3, production_line)
grip_sensor_3 = GripSensor("GS_003", "XYZ Robotics", robot_arm_3)

# Add the sensors to the robot arms
robot_arm_1.add_joint_consumption_sensor(current_sensor_1)
robot_arm_1.add_grip_sensor(grip_sensor_1)
robot_arm_2.add_joint_consumption_sensor(current_sensor_2)
robot_arm_2.add_grip_sensor(grip_sensor_2)
robot_arm_3.add_joint_consumption_sensor(current_sensor_3)
robot_arm_3.add_grip_sensor(grip_sensor_3)

# Start automatic data publishing for each sensor
current_sensor_1.start_auto_update()
grip_sensor_1.start_auto_update()

current_sensor_2.start_auto_update()
grip_sensor_2.start_auto_update()

current_sensor_3.start_auto_update()
grip_sensor_3.start_auto_update()


# Simulazione di attivazione/disattivazione della linea di produzione
# production_line.deactivate()  # Disattiva la linea di produzione (il sensore si ferma)
# time.sleep(5)
production_line.activate()  # Riattiva la linea di produzione (il sensore riparte)
# time.sleep(5)

# while production_line.active:
#     for robot_arm in production_line.robot_arms.values():
#         # print(robot_arm.get_json_joint_consumptions())        
#         print(robot_arm.get_json_grip())

# Loop di monitoraggio per stampare i dati
# while production_line.active:  # Usa production_line.active invece di self.active
#     for robot_arm in production_line.robot_arms.values():
#         for sensor in robot_arm.get_sensors():
#             print(sensor.get_json_measurement())  # Stampa i dati aggiornati

# # Avvio del client MQTT
production_line.start_mqtt_client()

# # Avvio del monitoraggio della produzione e pubblicazione dati sensori
production_line.monitor_and_publish()
