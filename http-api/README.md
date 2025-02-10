# HTTP-API

## Introduction

The HTTP-API microservice uses Flask to create a RESTful application. The application is structured such that every API request has
its dedicated resource. Furthermore, each resource has its HTTP methods declared, and each GET method has its Data
Transfer Object (DTO) defined to ensure the correct response.

## Server Application:

The "api_server.py" is the main entry point of the project. It contains the Flask application and the API resources. The
configuration is set in the "conf.yaml" file, but to assure a more robust approach, a default configuration dictionary
is also provided.

```bash
    configuration_dict = {
    "rest":{
        "api_prefix": DEFAULT_ENDPOINT_PREFIX,
        "host": "0.0.0.0",
        "port": 7070
    }
}
```

At the beginning, the program initializes one instance of the Flask application and one instance of the Flask-RESTful
API application:

```python
app = Flask(__name__)
api = Api(app)
```

#### Resources:

The API resources contains the models used to provide the clients with API methods, in this project they are defined
by :

- **ProductionLineResource**: Handles operations related to a production lines, such as declaring the basic number of
  robots and the status of the production line
- **RobotJointsConsumptionResource**: Handles the consumption of joints for a specific robot
- **RobotWeightEEResource**: Handles the end effector weight of a specific robot
- **FaultActuatorResource**: : Handles the notifications produced by the fault prevention actuator

Every resource is registered in the API resources using the Flask-RESTful method "api.add_resource()". Also, for each
resource the following are specified:

- The resource class.
- The endpoint URL.
- Arguments to be passed to the resource's constructor.
- A name for the endpoint.
- The supported HTTP methods.

Here, there is an example :

```python
api.add_resource(RobotJointsConsumptionResource,# resource class
    configuration_dict['rest']['api_prefix'] + '/robot/<string:robot_id>/telemetryjoints_consumption',
                # endpoint url
    resource_class_kwargs={'data_manager': data_manager},  # resource's constructor arguments
    endpoint="robot_joints_consumption",  # A name for the endpoint.
    methods=['GET', 'POST'])  # HTTP methods
```

#### Models:

Models contain the data structures for locations and devices. They are used by the resources to respond to POST requests
with the correct data format. In particular, we have two models in this project:

- **joint_model**.py: Contains the Joint class that represents an individual joint in a robotic arm, including
  its power consumption and a timestamp for data tracking

- **robot_arm_model**.py: Contains the RobotArmModel class, which represents a robotic arm with configurable properties,
  such as manufacturer details, joint information, and payload capacity.
  Here, there is an example :

```python
class JointsModel:

    def __init__(self, joint_id: str, consumption: float, timestamp: str):
        # joint information
        self.joint_id: str = joint_id
        self.set_consumption(consumption)
        self.set_timestamp(timestamp)

    # customization method example
    def set_consumption(self, consumption: float):
        ...

    def set_timestamp(self, timestamp: str):
        ...

    def to_json(self) -> str:
        ...
```

#### Data Transfer Objects (DTO):

DTOs contain the data models used to communicate with the external world. They are used by the resources to respond to
GET requests with the most suitable data format. In this project, we have two DTOs:

- joint_entity_response.py: Contains a structure for the information requested to understand a joint status

```python
    class JointEntityResponse:


def __init__(self, joint_id, consumption, timestamp):
    self.joint_id = joint_id
    self.consumption = consumption
    self.timestamp = timestamp
```

- robot_arm_entity_response.py: Contains the information required to understand a robotic arm status, including all of
  its joints information

```python
    class RobotArmEntityResponse:


def __init__(self, arm_id, manufacturer, number_of_joints):
    self.arm_id = arm_id
    self.manufacturer = manufacturer
    self.number_of_joints = number_of_joints


def to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__)
```

#### Persistence:

It contains the data access layer, it is used to handles the data regarding the joints and the end-effectors.

- data_manager.py: this file contains the DataManager class that provide methods to store permanently data, and also it
  provide various methods to retrieve these data in different structures.

```python
class DataManager:

    def __init__(self):
        """Initialize DataManager with empty data structures"""
        self.robot_arm_list = []  # List to store all robot arms
        self.joint_dictionary = {}  # Dictionary to store all joints by UUID
        self.weight_end_effector_dictionary = {}  # Dictionary to store end effector weight by robot ID
        self.fault_dictionary = {}  # Dictionary to store faults by robot ID
        self.status : bool = True # Production Line status
        self.line_id = "PL_001" # Production Line id

    # PRODUCTION LINE MANAGEMENT

    def update_production_line_info(self, line_id : str, status: bool):
        """
        Updates the production line information.

        :param line_id: The ID of the production line.
        :param status: The status of the production line
        """
        self.line_id = line_id
        self.status = status

    # SINGLE ROBOT ARM MANAGEMENT

    def add_robot_arm(self, new_robot_arm: RobotArmModel):
        ...

    def get_robot_arm(self, arm_id: str) -> RobotArmModel:
        ...

    # MULTIPLE ROBOT ARMS MANAGEMENT
    def get_all_robot_arms(self) -> list:
        ...

    # JOINT MANAGEMENT

    def add_joint_to_robot(self, arm_id: str, new_joint: JointsModel):
        ...

    def get_joints_for_robot(self, arm_id: str) -> list:
        ...

    # WEIGHT END EFFECTOR MANAGEMENT

    def set_end_effector_weight(self, arm_id: str, weight: float):
        ...

    def get_end_effector_weight(self, arm_id: str) -> float:
        ...

    # FAULT STATUS MANAGEMENT

    def set_robot_fault(self, arm_id: str, fault: str):
        ...

    def get_robots_fault(self):
        ...
```

#### Postman Collection:

In the Postman folder, you will find the complete Postman collection containing the configurations for all the available APIs in our application.

## Running the Service

### Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python api_server.py
   ```

### Dockerized

1. Build the Docker image:
   ```bash
   docker build -t http-api:0.1 .
   ```
2. Run the container:
   ```bash
   docker run -p 7070:7070 -v $(pwd)/test_conf.yaml:/app/conf.yaml http-api:0.1
   ```

## Deployment in Docker Compose

To integrate this microservice into a Docker Compose setup, ensure the following entry exists in `docker-compose.yml`:

```yaml
http-api:
  container_name: http-api
  image: http-api:0.1
  ports:
    - "7070:7070"
  volumes:
    - ./target_api_conf.yaml:/app/conf.yaml
  restart: always
  networks:
    - iot_production_line_network
```
