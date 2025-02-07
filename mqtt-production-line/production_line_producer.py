from model.robot_arm import RobotArm
from model.production_line import ProductionLine

# Robot Creation
robot_arm_1 = RobotArm("RA_001", "XYZ Robotics", 3, 1)
robot_arm_2 = RobotArm("RA_002", "XYZ Robotics", 3, 1)
robot_arm_3 = RobotArm("RA_003", "XYZ Robotics", 3, 1)

# Production Line Creation
production_line = ProductionLine("PL_001")

# Add robot arms to the production line
production_line.add_robot_arm(robot_arm_1)
production_line.add_robot_arm(robot_arm_2)
production_line.add_robot_arm(robot_arm_3)

# Start the production line
if __name__ == "__main__":
    try:
        production_line.activate()
        # Start the MQTT client
        production_line.start_mqtt_client()
        # Start the monitoring and publishing process
        production_line.monitor_and_publish()
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        # Ensure LWT message is sent and MQTT client is stopped
        production_line.stop_mqtt_client()