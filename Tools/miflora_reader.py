# -*- coding: utf-8 -*-


import sys
sys.path.append("/")
from AutomationTools.REST.server_connector import ServerConnector

from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from btlewrap.bluepy import BluepyBackend
from datetime import datetime
import json

import os.path
# API
#mb = StatusMessageBuilder()
SCRIPT_ID = 2

now = datetime.now().replace(microsecond=0).isoformat()

plants = [
            {"plant_id" : 1, "name" : "Cocos", "address" : "C4:7C:8D:66:ED:A8"},
            {"plant_id" : 2, "name" : "Strelitzia", "address" : "C4:7C:8D:66:EC:7C"},
            {"plant_id" : 3, "name" : "Ivy", "address" : "C4:7C:8D:66:F1:BD"}, # new borders!
            {"plant_id" : 4, "name" : "Alocasia", "address" : "C4:7C:8D:66:F0:D6"},
            {"plant_id" : 5, "name" : "Monstera_Delicoisa", "address" : "C4:7C:8D:66:F1:06"},
            {"plant_id" : 6, "name" : "Dracaena_Fragrans", "address" : "C4:7C:8D:66:F0:22"},
            {"plant_id" : 7, "name" : "Banana Terakota", "address" : "C4:7C:8D:66:F1:08"},
            {"plant_id" : 8, "name" : "Phoenix_Palm", "address" : "C4:7C:8D:66:ED:45"},
            {"plant_id" : 9, "name" : "Strelitzia (S)", "address" : "80:EA:CA:89:25:C4"},
            {"plant_id" : 10, "name" : "Banana White", "address" : "80:EA:CA:89:29:43"},
            {"plant_id" : 11, "name" : "Monstera (S)", "address" : "C4:7C:8D:66:F1:08"},
            {"plant_id" : 12, "name" : "Money Tree", "address" : "80:EA:CA:89:28:0C"},

            ]


def read_plant_data():
    for plant in plants:
        try:
            print(plant.get("address"))
            poller = MiFloraPoller(plant.get("address"), BluepyBackend)
            plantname = plant.get("name")

            print("---------" + plantname + "---------")
            print("FW: {}".format(poller.firmware_version()))
            #TODO: save in correct datatype
            print("Name: {}".format(poller.name()))
            print("Temperature: {}".format(poller.parameter_value(MI_TEMPERATURE)))
            print("Moisture: {}".format(poller.parameter_value(MI_MOISTURE)))
            print("Light: {}".format(poller.parameter_value(MI_LIGHT)))
            print("Conductivity: {}".format(poller.parameter_value(MI_CONDUCTIVITY)))
            print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))
            battery = "{}".format(poller.parameter_value(MI_BATTERY))
            version = "{}".format(poller.firmware_version())
            sunlight = "{}".format(poller.parameter_value(MI_LIGHT))
            temperature = "{}".format(poller.parameter_value(MI_TEMPERATURE))
            moisture = "{}".format(poller.parameter_value(MI_MOISTURE))
            fertility = "{}".format(poller.parameter_value(MI_CONDUCTIVITY))

            data = {}
            data['battery'] = battery
            data['version'] = version
            data['sunlight'] = sunlight
            data['temperature'] = temperature
            data['soil_moisture'] = moisture
            data['soil_fertility'] = fertility
            data['timestamp'] = str(now)
            data.update(plant)

            # if file doesn't exist create new (w+)
            with open("/AutomationTools/Resources/plant_data/" + plantname + ".json" , "w+") as json_file:
                json.dump(data, json_file, indent=4, sort_keys=True)
                json_file.close()
        except Exception as exception_message:
            print(exception_message)
            # mb.send_status_to_server(script_path=__file__, result=mb.fail, error_message=str(exception_message) + "Plant_with_Error: " + plantname, script_id=SCRIPT_ID)
            continue
    # mb.send_status_to_server(script_path=__file__, result=mb.successful, error_message="", script_id=SCRIPT_ID)


def send_plant_data(sc):
    try:
        for plant in plants:
            with open("/AutomationTools/Resources/plant_data/" + plant.get("name") + '.json') as f:
                file_data = json.load(f)
                sc.send_data_for_id(data_json=file_data, data_address="plant", data_id=plant.get("plant_id"))
    except Exception as exception_message:
        print(exception_message)
        # mb.send_status_to_server(script_path=__file__, result=mb.fail, error_message=str(exception_message), script_id=SCRIPT_ID)
    # mb.send_status_to_server(script_path=__file__, result=mb.successful, error_message="", script_id=SCRIPT_ID)

if __name__ == '__main__':
    read_plant_data()
    sc = ServerConnector()
    send_plant_data(sc)
