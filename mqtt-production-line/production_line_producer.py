"""
This script simulates a production line with multiple robot arms.
It manages the activation, deactivation, and monitoring of the production line and publishes data to an MQTT broker.
"""

import time
import paho.mqtt.client as mqtt
from model.robot_arm import RobotArm
from model.production_line import ProductionLine
import threading

# Create the robot arms
robot_arm_1 = RobotArm("RA_001", "XYZ Robotics", 3, 1)
robot_arm_2 = RobotArm("RA_002", "XYZ Robotics", 3, 1)
robot_arm_3 = RobotArm("RA_003", "XYZ Robotics", 3, 1)

# Create the production line
production_line = ProductionLine("PL_001")

# Add the robot arms to the production line
production_line.add_robot_arm(robot_arm_1)
production_line.add_robot_arm(robot_arm_2)
production_line.add_robot_arm(robot_arm_3)

# Flag for monitoring
monitoring_active = False


def activate_production_line():
    """
    Activates the production line and starts the monitoring thread.
    """
    global monitoring_active
    production_line.activate()  # Reactivate the production line
    print("Production line activated.")
    time.sleep(5)

    monitoring_active = True  # Enable monitoring
    start_monitoring_thread()  # Start the monitoring thread


def deactivate_production_line():
    """
    Deactivates the production line and stops the monitoring thread.
    """
    global monitoring_active
    production_line.deactivate()  # Deactivate the production line
    monitoring_active = False  # Stop monitoring
    production_line.stop_monitor_and_publish()  # Stop publishing data
    print("Production line stopped.")


def start_mqtt_client():
    """
    Starts the MQTT client and data publishing.
    """
    production_line.start_mqtt_client()  # Start the MQTT client
    # Monitor production and publish data
    production_line.monitor_and_publish()  # Start publishing data


def start_production_simulation():
    """
    Main function to manage the production simulation.
    """
    # Activate the production line
    activate_production_line()

    # Start the MQTT client and begin publishing data
    start_mqtt_client()


def start_monitoring_thread():
    """
    Starts the monitoring thread for the production line.
    """

    def monitor():
        while monitoring_active:  # Run while monitoring is active
            production_line.monitor_and_publish()  # Publish monitoring data
            time.sleep(3)  # Add a delay to avoid a too-fast loop

    # Start the monitoring thread
    monitoring_thread = threading.Thread(target=monitor)
    monitoring_thread.daemon = True  # The thread terminates when the main program ends
    monitoring_thread.start()


# Start the production simulation
if __name__ == "__main__":
    start_production_simulation()

    # Run an infinite loop to simulate continuous execution
    while True:
        time.sleep(1)  # Keep the main thread active
