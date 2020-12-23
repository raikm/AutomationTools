# -*- coding: utf-8 -*-

import sys
import requests
import configparser

sys.path.append("/")

from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from btlewrap.bluepy import BluepyBackend
from datetime import datetime

SCRIPT_ID = 2
now = datetime.now(tz=None).replace(microsecond=0).isoformat()
configParser = configparser.RawConfigParser()
configFilePath = r'../Resources/server_info.cfg'
configParser.read(configFilePath)
address = configParser.get('server', 'address')
port = configParser.get('server', 'port')

def get_plant_information():
    address = configParser.get('server', 'address')
    response = requests.get("http://" + address + ":" + port + "/getAllPlants/")
    return response.json()

def print_plant_data(plantname, poller):
    # TODO: save in correct datatype
    print("------" + plantname + "------")
    print("FW: {}".format(poller.firmware_version()))
    print("Name: {}".format(poller.name()))
    print("Temperature: {}".format(poller.parameter_value(MI_TEMPERATURE)))
    print("Moisture: {}".format(poller.parameter_value(MI_MOISTURE)))
    print("Light: {}".format(poller.parameter_value(MI_LIGHT)))
    print("Conductivity: {}".format(poller.parameter_value(MI_CONDUCTIVITY)))
    print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))

def read_plant_data():
    plants = get_plant_information()
    all_plant_data = {}

    for plant in plants:
        try:
            print(plant["address"])
            poller = MiFloraPoller(plant["address"], BluepyBackend)
            plantname = plant["name"]
            print_plant_data(plantname, poller)
            id = plant["id"]
            battery = "{}".format(poller.parameter_value(MI_BATTERY))
            version = "{}".format(poller.firmware_version())
            sunlight = "{}".format(poller.parameter_value(MI_LIGHT))
            temperature = "{}".format(poller.parameter_value(MI_TEMPERATURE))
            moisture = "{}".format(poller.parameter_value(MI_MOISTURE))
            fertility = "{}".format(poller.parameter_value(MI_CONDUCTIVITY))

            plant_data = {'plant_id': id, 'battery': battery, 'version': version, 'sunlight': sunlight, 'temperature': temperature,
                    'soil_moisture': moisture, 'soil_fertility': fertility, 'timestamp': str(now)}
            all_plant_data.update(plant_data)

        except Exception as exception_message:
            print(exception_message)
            #TODO: send error status to server
            continue
        send_plant_data(plant["id"], plant_data)

def send_plant_data(id, plant_data):
    response = requests.put(("http://" + address + ":" + port + "/plant/" + str(id) + "/"), data=plant_data)
    print(response.text)


if __name__ == '__main__':
    read_plant_data()
