"""
Module defines help methods for sending REST messages to Server

Author: R. Mueller 03.09.2019

"""


class RESTMessageBuilder(object):

    def __init__(self):
        pass
    # TODO: create Conncetor

    """POSSIBLE MESSAGE CODES"""
    SUCCESSFUL = "successful"

    ERROR_EXCEPTION_GENERAL = "exception was thrown"
    ERROR_FILE_NOT_FOUND = "file not found"
    UNKNOWN = "no success - no error code was found!"

    def send_status(self, message_code):
        print(str(message_code))
        message = self.get_code(message_code)
        print(message)

    def get_code(self, message_code):
        if message_code is 0:
            return self.SUCCESSFUL
        elif message_code is 1:
            return self.ERROR_FILE_NOT_FOUND
        elif message_code is 99:
            return self.ERROR_EXCEPTION_GENERAL
        else:
            return self.UNKNOWN

