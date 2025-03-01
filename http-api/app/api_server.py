from flask import Flask
from flask_restful import Api
from persistence.data_manager import DataManager
from resources.production_line_resource import ProductionLineResource
from resources.robot_joints_consumption_resource import RobotJointsConsumptionResource
from resources.robot_weight_ee_resource import RobotWeightEEResource
from resources.fault_actuator_resource import FaultActuatorResource
import yaml


# Default Values
CONF_FILE_PATH = "conf.yaml"
DEFAULT_ENDPOINT_PREFIX = "/api/v1/productionline"

# Default Configuration Dictionary
configuration_dict = {
    "rest": {
        "api_prefix": DEFAULT_ENDPOINT_PREFIX,
        "host": "0.0.0.0",
        "port": 7070
    }
}


# Read Configuration from target Configuration File Path
def read_configuration_file():
    """
    Reads the configuration from the specified YAML file and updates the global configuration dictionary.

    :return: The updated configuration dictionary.
    """
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
                 methods=['GET', 'POST'])

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

api.add_resource(FaultActuatorResource,
                 configuration_dict['rest']['api_prefix'] + '/robot/faults',
                 resource_class_kwargs={'data_manager': data_manager},
                 endpoint="fault_actuator",
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    # Run the Flask Application
    app.run(host=configuration_dict['rest']['host'], port=configuration_dict['rest']['port'])  # run our Flask app
