from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler
import os
import datetime
import shutil

#TODO: Automator: if file moved to desktop then run this script
SCRIPT_ID = 8

months = ["Unknown",
          "Januar",
          "Februar",
          "Maerz",
          "April",
          "Mai",
          "Juni",
          "Juli",
          "August",
          "September",
          "Oktober",
          "November",
          "Dezember"]



folder_to_track = '/Users/raik/Desktop'
now = datetime.datetime.now()
current_year = now.year
current_month = months[now.month]
#TODO: if new month not exist then create new folder
#current_month = "April"
current_bill_folder = "/Volumes/GoogleDrive/My Drive/_Unterlagen/Rechnungen/Rechnungen_" + str(current_year) + "/" + current_month + "_" + str(current_year)
folder_destination = current_bill_folder

#TODO: outsource to a method
for filename in os.listdir(folder_to_track):
    if "echnung_" not in filename:
        continue
    src = folder_to_track + "/" + filename
    newsrc = folder_destination + "/" + filename
    shutil.move(src, newsrc)