import aftership
import configparser

configParser = configparser.RawConfigParser()
configFilePath = r'../Resources/external_services.cfg'
configParser.read(configFilePath)

api_key = configParser.get('aftership', 'api_key')
aftership.api_key = api_key


def get_couriers():
    return aftership.courier.list_couriers()


# create package
def create_tracking(slug, tracking_number):
    tracking = {'slug': slug, 'tracking_number': tracking_number}
    result = aftership.tracking.create_tracking(tracking=tracking, timeout=10)
    return result['tracking']['id']


def update_tracking(tracking_id, **values):
    aftership.tracking.update_tracking(tracking_id=tracking_id, tracking=values)
    return True

# delete tracking
def get_tracking(tracking_id, fields=None):
    try:
        result = aftership.tracking.get_tracking(tracking_id=tracking_id, fields=','.join(fields))
    except aftership.exception.NotFound:
        return None

    return result['tracking']


def delete_tracking(tracking_id):
    try:
        aftership.tracking.delete_tracking(tracking_id=tracking_id)
    except aftership.exception.NotFound:
        return False
    return True
