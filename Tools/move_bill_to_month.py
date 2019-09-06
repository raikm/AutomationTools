from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler
import os
import datetime
import shutil


months = ["Unknown",
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            if "Rechnung_" not in filename:
                continue
            src = folder_to_track + "/" + filename
            newsrc = folder_destination + "/" + filename
            shutil.move(src, newsrc)


folder_to_track = '/Users/raik/Desktop'
now = datetime.datetime.now()
current_year = now.year
current_month = months[now.month]
current_bill_folder = "/Volumes/GoogleDrive/My Drive/_Unterlagen/Rechnungen/Rechnungen_" + str(current_year) + "/" + current_month + "_" + str(current_year)
folder_destination = current_bill_folder
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
        print("run")
except KeyboardInterrupt:
    observer.stop()

observer.join()
