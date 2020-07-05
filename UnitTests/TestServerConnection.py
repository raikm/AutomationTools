from REST.message_builder import RESTMessageBuilder
import unittest


class TestStringMethods(unittest.TestCase):

    def test_send_status_to_server(self):
        rest_builder = RESTMessageBuilder()
        rest_builder.send_status_to_server(script_path="testpath",result=rest_builder.successful, error_message="",
                                           script_id=1)


if __name__ == '__main__':
    unittest.main()