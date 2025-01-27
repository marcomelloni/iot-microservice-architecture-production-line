from web_server import WebServer

WEB_CONFIG_FILE = "web_conf.yaml"

if __name__ == '__main__':

    # Create Web Server
    web_server = WebServer(WEB_CONFIG_FILE)

    # Run Web Server
    web_server.start()