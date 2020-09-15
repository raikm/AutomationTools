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
            {"plant_id" : 1, "name" : "Cocos", "address" : "C4:7C:8D:66:ED:A8", "soil_moisture_borders": {"min": 15, "max": 60, "currency" : "%"}, "soil_fertitlity_borders": {"min":350, "max": 2000, "currency" : "µS/cm"}, "sunlight_intensity_borders": {"min": 4000, "max": 75000, "currency" : "lux"}, "temperature_borders": {"min": 5, "max": 35, "currency" : "°C"}},
            {"plant_id" : 2, "name" : "Strelitzia", "address" : "C4:7C:8D:66:EC:7C", "soil_moisture_borders": {"min": 15, "max": 60, "currency" : "%"}, "soil_fertitlity_borders": {"min": 350, "max": 2000, "currency" : "µS/cm"}, "sunlight_intensity_borders": {"min": 2500, "max": 300000, "currency" : "lux"}, "temperature_borders": {"min": 15, "max": 60, "currency" : "°C"}},
            {"plant_id" : 3, "name" : "Schefflera", "address" : "C4:7C:8D:66:F1:BD", "soil_moisture_borders": {"min": 15, "max": 60, "currency" : "%"}, "soil_fertitlity_borders": {"min": 350, "max": 2000, "currency" : "µS/cm"}, "sunlight_intensity_borders": {"min": 1000, "max": 18000, "currency" : "lux"}, "temperature_borders": {"min": 6, "max": 32, "currency" : "°C"}},
            {"plant_id" : 4, "name" : "Alocasia", "address" : "C4:7C:8D:66:F0:D6", "soil_moisture_borders": {"min": 15, "max": 60, "currency" : "%"}, "soil_fertitlity_borders": {"min": 350, "max": 2000, "currency" : "µS/cm"}, "sunlight_intensity_borders": {"min": 1000, "max": 22500, "currency" : "lux"}, "temperature_borders": {"min": 10, "max": 32, "currency" : "°C"}},
            {"plant_id" : 5, "name" : "Monstera_Delicoisa", "address" : "C4:7C:8D:66:F1:06", "soil_moisture_borders": {"min": 15, "max": 60, "currency" : "%"}, "soil_fertitlity_borders": {"min": 350, "max": 2000, "currency" : "µS/cm"}, "sunlight_intensity_borders": {"min": 800, "max": 15000, "currency" : "lux"}, "temperature_borders": {"min": 12, "max": 32, "currency" : "°C"}},
            {"plant_id" : 6, "name" : "Dracaena_Fragrans", "address" : "C4:7C:8D:66:F0:22", "soil_moisture_borders": {"min": 15, "max": 60, "currency" : "%"}, "soil_fertitlity_borders": {"min": 200, "max": 1500, "currency" : "µS/cm"}, "sunlight_intensity_borders": {"min": 2000, "max": 50000, "currency" : "lux"}, "temperature_borders": {"min": 10, "max": 35, "currency" : "°C"}},
            {"plant_id" : 7, "name" : "Banana", "address" : "C4:7C:8D:66:F1:08", "soil_moisture_borders": {"min": 15, "max": 60, "currency" : "%"}, "soil_fertitlity_borders": {"min": 350, "max": 2000, "currency" : "µS/cm"}, "sunlight_intensity_borders": {"min": 4000, "max": 45000, "currency" : "lux"}, "temperature_borders": {"min": 5, "max": 35, "currency" : "°C"}},
            {"plant_id" : 8, "name" : "Phoenix_Palm", "address" : "C4:7C:8D:66:ED:45", "soil_moisture_borders": {"min": 15, "max": 60, "currency" : "%"}, "soil_fertitlity_borders": {"min": 350, "max": 2000, "currency" : "µS/cm"}, "sunlight_intensity_borders": {"min": 3700, "max": 60000, "currency" : "lux"}, "temperature_borders": {"min": 5, "max": 35, "currency" : "°C"}},
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
    #read_plant_data()
    sc = ServerConnector()
    send_plant_data(sc)
