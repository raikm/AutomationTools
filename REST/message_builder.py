"""
Module defines help methods for sending REST messages to Server

Author: R. Mueller 03.09.2019

"""
from REST.server_connector import ServerConnector
import json
import os
from datetime import datetime

timestamp = datetime.now().replace(microsecond=0).isoformat()


class RESTMessageBuilder(object):
    SERVER_ADDRESS = "http://localhost:8080/HomeAPI/rest/" #TODO: make more generic and not hard coded here

    def __init__(self):
        self.server = ServerConnector(self.SERVER_ADDRESS)
        self.successful = "successful"
        self.fail = "fail"

    def send_status_to_server(self, script_path, result, error_message):
        status_code = 1
        if result == self.successful:
            status_code = 0
        script_name = self.get_filename_without_extension(script_path)
        data = {"script": script_name, "script_path": script_path, "status_code": status_code, "status": result, "error": error_message,
                "timestamp": timestamp}
        data_json = json.dumps(data)
        self.server.send_status(data_json)

    @staticmethod
    def get_filename_without_extension(file_path):
        file_basename = os.path.basename(file_path)
        filename_without_extension = file_basename.split('.')[0]
        return filename_without_extension
