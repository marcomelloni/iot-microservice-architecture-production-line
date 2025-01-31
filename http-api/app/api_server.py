from flask import Flask
from flask_restful import Api
from persistence.data_manager import DataManager
from resources.production_line_resource import ProductionLineResource
from resources.robot_joints_consumption_resource import RobotJointsConsumptionResource
from resources.robot_weight_ee_resource import RobotWeightEEResource
import yaml
from model.robot_arm_model import RobotArmModel
from model.joints_model import JointsModel

# Default Values
CONF_FILE_PATH = "conf.yaml"
DEFAULT_ENDPOINT_PREFIX = "/api/v1/productionline"

# Default Configuration Dictionary
configuration_dict = {
    "rest":{
        "api_prefix": DEFAULT_ENDPOINT_PREFIX, 
        "host": "0.0.0.0",
        "port": 7070
    }
}

# Read Configuration from target Configuration File Path
def read_configuration_file():
    global configuration_dict

    with open(CONF_FILE_PATH, 'r') as file:
        configuration_dict = yaml.safe_load(file)

    return configuration_dict

# Read Configuration file
configuration_dict = read_configuration_file()

print("Read Configuration from file ({}): {}".format(CONF_FILE_PATH, configuration_dict))

app = Flask(__name__)
api = Api(app)

print("Starting HTTP RESTful API Server ...")

data_manager = DataManager()

# Add Resources and Endpoints
api.add_resource(ProductionLineResource, 
                  configuration_dict['rest']['api_prefix'] + '/robots',
                  resource_class_kwargs={'data_manager': data_manager},
                  endpoint="productionline",
                  methods=['GET'])


api.add_resource(RobotJointsConsumptionResource, 
                  configuration_dict['rest']['api_prefix'] + '/robot/<string:robot_id>/telemetry/joints_consumption',
                  resource_class_kwargs={'data_manager': data_manager},
                  endpoint="robot_joints_consumption",
                  methods=['GET', 'POST'])


api.add_resource(RobotWeightEEResource, 
                  configuration_dict['rest']['api_prefix'] + '/robot/<string:robot_id>/telemetry/weight_ee',
                  resource_class_kwargs={'data_manager': data_manager},
                  endpoint="robot_weight_ee",
                  methods=['GET', 'POST'])


if __name__ == '__main__':

    # # Creare un braccio robotico
    # robot1 = RobotArmModel(arm_id="arm1", manufacturer="RobotCo")
    # robot2 = RobotArmModel(arm_id="arm2", manufacturer="ABB")
    # robot3 = RobotArmModel(arm_id="arm3", manufacturer="FANUC")
    # data_manager.add_robot_arm(robot1)
    # data_manager.add_robot_arm(robot2)
    # data_manager.add_robot_arm(robot3)

    # # Creare un giunto e aggiungerlo al braccio robotico
    # joint1 = JointsModel(joint_id="joint1", consumption=100.0, timestamp="2024-01-31T12:00:00")
    # joint2 = JointsModel(joint_id="joint2", consumption=109.0, timestamp="2024-01-31T16:00:00")
    # joint1_1 = JointsModel(joint_id="joint1_1", consumption=2.0, timestamp="2024-01-31T16:00:00")
    # joint2_1 = JointsModel(joint_id="joint1_1", consumption=157.0, timestamp="2024-01-31T16:00:00")
    # data_manager.add_joint_to_robot("arm1", joint1)
    # data_manager.add_joint_to_robot("arm1", joint2)
    # data_manager.add_joint_to_robot("arm2", joint1_1)
    # data_manager.add_joint_to_robot("arm2", joint2_1)

    # # Impostare il peso dell'end effector per un robot
    # data_manager.set_end_effector_weight("arm1", 5.0)
    # data_manager.set_end_effector_weight("arm2", 75.0)
    # data_manager.set_end_effector_weight("arm3", 15.0)

    # Run the Flask Application
    app.run(host=configuration_dict['rest']['host'], port=configuration_dict['rest']['port'])  # run our Flask app