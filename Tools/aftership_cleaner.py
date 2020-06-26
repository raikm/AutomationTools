from Aftership.package_tracker_manager import cleanup_delivered_trackings, delete_tracking
from datetime import datetime, timedelta, timezone
from REST.message_builder import RESTMessageBuilder


mb = RESTMessageBuilder()
trackings = cleanup_delivered_trackings()
if trackings is None:
    exit()


def check_package_info(status, date):
    time_between = datetime.now() - date
    if status == "Delivered" and time_between.days > 4:
        return True
    elif status == "Pending" and time_between.days > 14:
        return True
    else:
        return False


try:
    for tracking in trackings:

        shipment_delivery_date_str = tracking['shipment_delivery_date']
        updated_at_date_str = tracking['updated_at']
        shipment_status = tracking['tag']

        if shipment_delivery_date_str is None:
            updated_at_date = datetime.strptime(updated_at_date_str, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
            if check_package_info(shipment_status, updated_at_date):
                delete_tracking(tracking_id=tracking['id'])

        else:
            shipment_delivery_date = datetime.strptime(shipment_delivery_date_str, '%Y-%m-%dT%H:%M:%S')
            if check_package_info(shipment_status, shipment_delivery_date):
                delete_tracking(tracking_id=tracking['id'])

        mb.send_status_to_server(script_path=__file__, result=mb.successful,
                                                 error_message="")
except Exception as e:
    mb.send_status_to_server(script_path=__file__, result=mb.fail,
                                             error_message=str(e))

mb.send_status_to_server(script_path=__file__, result=mb.successful,
                                                 error_message="")