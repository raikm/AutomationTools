"""
Module defines help methods for sending REST messages to Server

Author: R. Mueller 03.09.2019

"""
from REST.server_connector import ServerConnector
import json
import os
from datetime import datetime

SUCCESSFUL = "successful"
timestamp = datetime.now().replace(microsecond=0).isoformat()

class RESTMessageBuilder(object):
    SERVER_ADDRESS = "http://192.168.0.34:8080/HomeAPI/rest/"

    def __init__(self):
        self.server = ServerConnector(self.SERVER_ADDRESS)

    def build_status_message(self, script_path, message):
        message_code = 1
        if SUCCESSFUL in message:
            message_code = 0
        script_name = self.get_filename_without_extension(script_path)
        data = {"script": script_name, "script path": script_path, "status code": message_code, "status": message, "timestamp": timestamp}
        data_json = json.dumps(data)
        self.server.send_status(data_json)

    @staticmethod
    def get_filename_without_extension(file_path):
        file_basename = os.path.basename(file_path)
        filename_without_extension = file_basename.split('.')[0]
        return filename_without_extension
