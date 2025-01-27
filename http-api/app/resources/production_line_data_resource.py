from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource

class ProductionLineDataResource(Resource):
    """Resource to handle the Data of a specific Production Line"""

    def __init__(self, **kwargs):
        # Inject the DataManager instance
        self.data_manager = kwargs['data_manager']

    def get(self, device_id):
        """GET Request to retrieve the Telemetry Data of a target device"""
        return '', 501

    def post(self, device_id):
       return '', 501

