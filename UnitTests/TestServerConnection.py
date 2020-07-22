import unittest
import Tools.miflora_reader as miflora
from REST.server_connector import ServerConnector


class TestStringMethods(unittest.TestCase):



    # def test_send_status_to_server(self):
    #     rest_builder = RESTMessageBuilder()
    #     rest_builder.send_status_to_server(script_path="testpath",result=rest_builder.successful, error_message="",
    #                                        script_id=1)
    #
    # def test_send_plant_data_to_server(self):
    #     sc = ServerConnector()
    #     miflora.send_plant_data(sc)

    def test_read_plant_data(self):
        miflora.read_plant_data();

    # def test_get_plant_detail_data(self):
    #     sc = ServerConnector()
    #     sc.get_data("plant", 1)
    #
    # def test_get_all_plant_detail_data(self):
    #     sc = ServerConnector()
    #     sc.get_data("allplants")

if __name__ == '__main__':
    unittest.main()