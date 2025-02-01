import requests
from flask import Flask, request, render_template
import os
import yaml
import threading


class WebServer:

    def __init__(self, config_file:str):

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
        self.app.add_url_rule('/robot/<string:robot_id>/telemetry/joints_consumption', 'joint_consumption', self.joint_consumption)
        self.app.add_url_rule('/robot/<string:robot_id>/telemetry/weight_ee', 'weight_ee', self.weight_ee)
        self.app.add_url_rule('/robots', 'robots', self.robots)

    def read_configuration_file(self):
        """ Read Configuration File for the Web Server
         :return:
        """

        # Get the main communication directory
        main_app_path = ""

        # Construct the file path
        file_path = os.path.join(main_app_path, self.config_file)

        with open(file_path, 'r') as file:
            self.configuration_dict = yaml.safe_load(file)

        print("Read Configuration from file ({}): {}".format(self.config_file, self.configuration_dict))
        
    def joint_consumption(self, robot_id):
        """ Get telemetry data for a specific device and render the telemetry.html template"""
        joint_consumption_values = self.http_get_production_line_joint_consumption_data(robot_id)
        print(joint_consumption_values)

        # Prepara una lista di consumi con joint_id e valore di consumo
        joints = [{"joint_id": joint["joint_id"], "consumption": joint["consumption"]} for joint in joint_consumption_values]

        return render_template('joint_consumption.html', joints=joints, robot_id=robot_id)

    def http_get_production_line_joint_consumption_data(self, robot_id):
        """ Get all locations from the remote server over HTTP"""

        # Get the base URL from the configuration
        base_http_url = self.configuration_dict['web']['api_base_url']
        target_url = f'{base_http_url}/robot/{robot_id}/telemetry/joints_consumption'

        # Send the GET request
        response_string = requests.get(target_url)

        # Return the JSON response
        return response_string.json()

    def weight_ee(self, robot_id):
        """ Get the weight supported by the end effector of a robot"""
        weight_value = self.http_get_production_line_weight_ee_data(robot_id)
        return render_template('weight_ee.html', weight_value=weight_value, robot_id=robot_id)

    def http_get_production_line_weight_ee_data(self, robot_id):
        """ Get all devices for the target location_id from the remote server over HTTP"""

        # Get the base URL from the configuration
        base_http_url = self.configuration_dict['web']['api_base_url']
        target_url = f'{base_http_url}/robot/{robot_id}/telemetry/weight_ee'

        # Send the GET request
        response_string = requests.get(target_url)

        # Return the JSON response
        return response_string.json()

    def robots(self):
        """ Get all robots"""
        robots = self.http_get_robots_data()
        return render_template('robots.html', value=robots)

    def http_get_robots_data(self):
        """ Get all devices for the target location_id from the remote server over HTTP"""

        # Get the base URL from the configuration
        base_http_url = self.configuration_dict['web']['api_base_url']
        target_url = f'{base_http_url}/robots'

        # Send the GET request
        response_string = requests.get(target_url)

        # Return the JSON response
        return response_string.json()

    def run_server(self):
        """ Run the Flask Web Server"""
        self.app.run(host=self.configuration_dict['web']['host'], port=self.configuration_dict['web']['port'])

    def start(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def stop(self):
        """ Stop the REST API Server (Flask Method)
        In this code, request.environ.get('werkzeug.server.shutdown')
        retrieves the shutdown function from the environment.
        If the function is not found, it raises a RuntimeError,
        indicating that the server is not running with Werkzeug.
        If the function is found, it is called to shut down the server."""

        # Shutdown the server
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')

        # Call the shutdown function
        func()

        # Wait for the server thread to join
        self.server_thread.join()