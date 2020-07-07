from Tools.status_message_builder import StatusMessageBuilder

destination_folder = "/Users/raik/Backups/openhab/"

#               user,         ip address,     ssh key path,                backup folder
raspberries = [("openhabian", "192.168.0.14", "~/.ssh/openhab/openhabkey", "/var/lib/openhab2/backups")]
SUCCESSFUL = "successful"

SCRIPT_ID = 6

def get_backup():
    rest_builder = StatusMessageBuilder()

    #todo test connection first!

 #   try:
        # for raspberry in raspberries:
        #
        #     command = "scp -i " + raspberry[2] + " -r " + raspberry[0] + "@" + raspberry[1] + ":" + raspberry[3] + " " + destination_folder
        #     output = subprocess.Popen(command,
        #                               shell=True,
        #                               stdin=subprocess.PIPE,
        #                               stdout=subprocess.PIPE,
        #                               stderr=subprocess.PIPE)
        #
        #     stdout_value, stderr_value = output.communicate()

    # except Exception as e:
    #     rest_builder.build_status_message(script_path=__file__, message=e)
    # except (NewConnectionError, MaxRetryError, ConnectTimeoutError) as e:
    #     rest_builder.build_status_message(script_path=__file__, message=e)

    #if stderr_value:
    #    rest_builder.build_status_message(script_path=__file__, message=stderr_value.split('\r\n')[0])
    #else:
    rest_builder.send_status_to_server(script_path=__file__, message=SUCCESSFUL)
    clean_up_local_backup_folder(destination_folder)


def clean_up_local_backup_folder(folder):
    # TODO check the dates and delete older than 2 months
    pass


get_backup()
