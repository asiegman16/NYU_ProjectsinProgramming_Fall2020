#!/Users/siegmanA/anaconda3/bin/python

import sqlite3
import time
import json
import urllib.request
from datetime import datetime


with urllib.request.urlopen("https://feeds.citibikenyc.com/stations/stations.json") as url:
    data = json.loads(url.read().decode())

stations = data['stationBeanList']

con = sqlite3.connect('/Users/siegmanA/Desktop/NYU-Projects-in-Programming-Fall-2019/(Class 7) Data Visualization/citibikeDataForViz.db') 

query_template = """INSERT OR IGNORE INTO StationsData(station_id, stationName, availableDocks, totalDocks, latitude, \
longitude, statusValue, statusKey, availableBikes, stAddress1, stAddress2, city, postalCode, location, altitude, \
testStation, lastCommunicationTime, landMark) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

for entry in stations: 
    station_id = int(entry['id']) 
    stationName = str(entry['stationName'])
    availableDocks = int(entry['availableDocks'])
    totalDocks = int(entry['totalDocks'])
    latitude = str(entry['latitude'])
    longitude = str(entry['longitude'])
    statusValue = str(entry['statusValue'])
    statusKey = int(entry['statusKey'])
    availableBikes = int(entry['availableBikes'])
    stAddress1 = str(entry['stAddress1'])
    stAddress2 = str(entry['stAddress2'])
    city = str(entry['city'])
    postalCode = str(entry['postalCode'])
    location = str(entry['location'])
    altitude = str(entry['altitude'])
    testStation = bool(entry['testStation'])
    lastCommunicationTime = entry['lastCommunicationTime']
    landMark = str(entry['landMark'])

    query_parameters = (station_id, stationName, availableDocks, totalDocks, latitude, longitude, statusValue, statusKey, availableBikes, stAddress1, stAddress2, city, postalCode, location, altitude, testStation, lastCommunicationTime, landMark)

    con.execute(query_template, query_parameters)

con.commit()

print("Success!")

time.sleep(15)
