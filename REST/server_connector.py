"""
Interaction with the Server (REST API)

Author: R. Mueller 03.09.2019

"""
import requests


class ServerConnector(object):

    def __init__(self):
        self.address = "http://localhost:8000/"
        # self.test_connection()

    def test_connection(self):
        try:
            resp = requests.get(self.address)
            if resp.status_code != 200:
                print(resp.status_code)
                return 1
        except Exception as e:
            print(e) # TODO: send Mail
            return 1
        return 0

    def send_script_status(self, data_json, script_id):
        try:
            address = self.address + "scriptstatus/" + str(script_id) + "/"
            requests.put(address, data=data_json)
        except Exception as e:
            print(e) #TODO

    def send_data_for_id(self, data_json, data_address, data_id):
        try:
            address = self.address + data_address + "/" + str(data_id) + "/"
            response = requests.put(address, data=data_json)
            print(response.text)
        except Exception as e:
            print(e)

    def get_data(self, data_address, data_id):
        try:
            address = self.address + data_address + "/" + str(data_id) + "/"
            response = requests.get(address)
            print(response.text)
        except Exception as e:
            print(e)

    def get_data(self, data_address):
        try:
            address = self.address + data_address + "/"
            response = requests.get(address)
            print(response.text)
        except Exception as e:
            print(e)