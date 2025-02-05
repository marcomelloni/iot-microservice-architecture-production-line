"""
This script initializes and starts the web server for the production line control system.
"""

from web_server import WebServer

# Path to the web server configuration file
WEB_CONFIG_FILE = "web_conf.yaml"

if __name__ == '__main__':
    # Create an instance of the WebServer with the specified configuration file
    web_server = WebServer(WEB_CONFIG_FILE)

    # Start the web server
    web_server.start()
