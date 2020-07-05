"""
Module defines help methods for sending REST messages to Server

Author: R. Mueller 03.09.2019

"""
from REST.server_connector import ServerConnector
import json
import os
from datetime import datetime




class RESTMessageBuilder(object):
    SERVER_ADDRESS = "http://localhost:8080/HomeAPI/rest/" #TODO: make more generic and not hard coded here

    def __init__(self):
        self.server = ServerConnector(self.SERVER_ADDRESS)
        self.successful = "successful"
        self.fail = "fail"

    def send_status_to_server(self, script_path, result, error_message, script_id):
        status_code = 1
        if result == self.successful:
            status_code = 0
        script_name = self.get_filename_without_extension(script_path)
        timestamp = datetime.now()
        data = {"script_id": script_id, "name": script_name, "script_path": script_path, "status_code": status_code, "status_text": result, "error_text": error_message,
                "timestamp": timestamp}
        self.server.send_status(data, script_id)

    @staticmethod
    def get_filename_without_extension(file_path):
        file_basename = os.path.basename(file_path)
        filename_without_extension = file_basename.split('.')[0]
        return filename_without_extension
