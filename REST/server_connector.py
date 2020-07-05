"""
Interaction with the Server (REST API)

Author: R. Mueller 03.09.2019

"""
import requests


class ServerConnector(object):

    def __init__(self, address=None):
        self.address = address
        # self.test_connection()

    @staticmethod
    def test_connection():
        try:
            address = "http://localhost:8080/HomeAPI/rest/server/status"
            resp = requests.get(address)
            if resp.status_code != 200:
                print(resp.status_code)
                return 1
        except Exception as e:
            print(e)
            # TODO: send Mail
            return 1
        return 0

    def send_status(self, data_json, script_id):
        try:
            # print(data_json)  # DEBUG
            address = "http://127.0.0.1:8000/scriptstatus/" + str(script_id) + "/"
            response = requests.put(address, data=data_json)
            print(response.text)
        except Exception as e:
            print(e)
