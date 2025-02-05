import requests
from flask import Flask, request, render_template
import os
import yaml
import threading


class WebServer:
    """
    Represents a web server for the production line control system.
    Manages the configuration, Flask app setup, and routes for telemetry data.
    """

    def __init__(self, config_file: str):
        """
        Initializes the web server with configuration settings and sets up the Flask app.
        """
        # Server Thread
        self.server_thread = None

        # Save the configuration file
        self.config_file = config_file

        # Get the main communication directory
        main_app_path = ""

        # Construct the file path
        template_dir = os.path.join(main_app_path, 'templates')

        # Set a default configuration
        self.configuration_dict = {
            "web": {
                "host": "0.0.0.0",
                "port": 7071,
                "api_base_url": "http://127.0.0.1:7070/api/v1/productionline"
            }
        }

        # Read Configuration from target Configuration File Path
        self.read_configuration_file()

        # Create the Flask app
        self.app = Flask(__name__, template_folder=template_dir)

        # Add URL rules to the Flask app mapping the URL to the function
        self.app.add_url_rule('/robot/<string:robot_id>/telemetry/joints_consumption', 'joint_consumption',
                              self.joint_consumption)
        self.app.add_url_rule('/robot/<string:robot_id>/telemetry/weight_ee', 'weight_ee', self.weight_ee)
        self.app.add_url_rule('/robots', 'robots', self.robots)
        self.app.add_url_rule('/faults', 'faults', self.faults)

    def read_configuration_file(self):
        """
        Reads the configuration file for the web server.
        """
        # Get the main communication directory
        main_app_path = ""

        # Construct the file path
        file_path = os.path.join(main_app_path, self.config_file)

        with open(file_path, 'r') as file:
            self.configuration_dict = yaml.safe_load(file)

        print("Read Configuration from file ({}): {}".format(self.config_file, self.configuration_dict))

    def joint_consumption(self, robot_id):
        """
        Gets telemetry data for a specific device and renders the telemetry.html template.
        """
        joint_consumption_values = self.http_get_production_line_joint_consumption_data(robot_id)
        print(joint_consumption_values)

        # Prepares a list of consumptions with joint_id and consumption value
        joints = [{"joint_id": joint["joint_id"], "consumption": joint["consumption"]} for joint in
                  joint_consumption_values]

        return render_template('joint_consumption.html', joints=joints, robot_id=robot_id)

    def http_get_production_line_joint_consumption_data(self, robot_id):
        """
        Gets all locations from the remote server over HTTP.
        """
        # Get the base URL from the configuration
        base_http_url = self.configuration_dict['web']['api_base_url']
        target_url = f'{base_http_url}/robot/{robot_id}/telemetry/joints_consumption'

        # Send the GET request
        response_string = requests.get(target_url)

        # Return the JSON response
        return response_string.json()

    def weight_ee(self, robot_id):
        """
        Gets the weight supported by the end effector of a robot and renders the weight_ee.html template.
        """
        weight_value = self.http_get_production_line_weight_ee_data(robot_id)
        return render_template('weight_ee.html', weight_value=weight_value, robot_id=robot_id)

    def http_get_production_line_weight_ee_data(self, robot_id):
        """
        Gets the weight supported by the end effector from the remote server over HTTP.
        """
        # Get the base URL from the configuration
        base_http_url = self.configuration_dict['web']['api_base_url']
        target_url = f'{base_http_url}/robot/{robot_id}/telemetry/weight_ee'

        # Send the GET request
        response_string = requests.get(target_url)

        # Return the JSON response
        return response_string.json()

    def robots(self):
        """
        Gets all robots and renders the robots.html template.
        """
        robots = self.http_get_robots_data()
        return render_template('robots.html', value=robots)

    def http_get_robots_data(self):
        """
        Gets all robots from the remote server over HTTP.
        """
        # Get the base URL from the configuration
        base_http_url = self.configuration_dict['web']['api_base_url']
        target_url = f'{base_http_url}/robots'

        # Send the GET request
        response_string = requests.get(target_url)

        # Return the JSON response
        return response_string.json()

    def faults(self):
        """
        Gets all faults and renders the faults.html template.
        """
        faults = self.http_get_faults_data()
        return render_template('faults.html', value=faults)

    def http_get_faults_data(self):
        """
        Gets all faults from the remote server over HTTP.
        """
        # Get the base URL from the configuration
        base_http_url = self.configuration_dict['web']['api_base_url']
        target_url = f'{base_http_url}/robot/faults'

        # Send the GET request
        response_string = requests.get(target_url)

        # Return the JSON response
        return response_string.json()

    def run_server(self):
        """
        Runs the Flask web server.
        """
        self.app.run(host=self.configuration_dict['web']['host'], port=self.configuration_dict['web']['port'])

    def start(self):
        """
        Starts the web server in a separate thread.
        """
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def stop(self):
        """
        Stops the REST API server (Flask method).
        """
        # Shutdown the server
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')

        # Call the shutdown function
        func()

        # Wait for the server thread to join
        self.server_thread.join()
