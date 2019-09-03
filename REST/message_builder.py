"""
Module defines help methods for sending REST messages to Server

Author: R. Mueller 03.09.2019

"""
from REST.server_connector import ServerConnector
import json


class RESTMessageBuilder(object):
    SERVER_ADDRESS = "http://192.168.0.34:8080/HomeAPI/rest/"
    """POSSIBLE MESSAGE CODES"""
    SUCCESSFUL = "successful"

    ERROR_EXCEPTION_GENERAL = "exception was thrown"
    ERROR_FILE_NOT_FOUND = "file not found"
    UNKNOWN = "No success - no error code was found!"

    def __init__(self):
        self.server = ServerConnector(self.SERVER_ADDRESS)
        response = self.server.test_connection()
        if response is not 0:
            print("No connection to server is provided!")

    def build_status_message(self, message_code):
        print(str(message_code))
        message = self.get_code(message_code)
        print(message)
        # TODO build proper JSON Data
        data = {"data": "24.3"}
        data_json = json.dumps(data)
        self.server.send_status(data_json)

    def get_code(self, message_code):
        if message_code is 0:
            return self.SUCCESSFUL
        elif message_code is 1:
            return self.ERROR_FILE_NOT_FOUND
        elif message_code is 99:
            return self.ERROR_EXCEPTION_GENERAL
        else:
            return self.UNKNOWN
