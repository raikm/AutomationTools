"""
Interaction with the Server (REST API)

Author: R. Mueller 03.09.2019

"""
import requests


class ServerConnector(object):

    def __init__(self, address=None):
        self.address = address

    @staticmethod
    def test_connection():
        try:
            address = "http://192.168.0.34:8080/HomeAPI/rest/server/status"
            resp = requests.get(address)
            if resp.status_code != 200:
                print(resp.status_code)
                return 1
        except Exception as e:
            print(e)
            return 1
        return 0

    def send_status(self, data_json):
        if self.test_connection() is 0:
            print(data_json)
            address = self.address + "status"
            response = requests.post(address, data=data_json)
            print response.text
