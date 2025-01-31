# Project Structure

The project is structured as follows:

### Server Application:

- api_server.py: The main entry point of the project. It contains the Flask application and the API resources.

### Resources: Contains the API resources for the locations and devices.

### Models: Contains the data models for the locations and devices. Detailed in the following files:

- jont_model.py: Contains the Joint class that represents the joint consumptions of a specific robot arm.
- weight_ee.py: Contains the Ee class that represents the end effector of a robot arm.ù

### DTO: Contains the Data Transfer Objects (DTOs) for the joints and EEs. Detailed in the following files:

### Persistence: Contains the data access layer for the locations and devices. Detailed in the following file:

- data_manager.py: Contains the DataManager class that handles the data access layer for the joints and EEs.

### Clients: Contains the client to interact with the API. Detailed in the following file:
