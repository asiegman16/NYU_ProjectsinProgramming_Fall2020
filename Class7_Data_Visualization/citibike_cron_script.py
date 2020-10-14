#!/Users/siegmanA/anaconda3/bin/python

import sqlite3
import time 
import json 
import urllib.request
from datetime import datetime

con = sqlite3.connect('/Users/siegmanA/Desktop/NYU_ProjectsinProgramming_Fall2020/Class7_Data_Visualization/citibikeData2020_Class7.db')


with urllib.request.urlopen("https://gbfs.citibikenyc.com/gbfs/en/station_status.json") as url:
    data = json.loads(url.read().decode())

values_list = list(data.values())

clean_data = values_list[0]['stations']

query_template = """INSERT OR IGNORE INTO StationsData(station_id, num_ebikes_available, num_bikes_available, \
is_installed, last_reported, num_docks_disabled, is_renting, eightd_has_available_keys, \
num_docks_available, num_bikes_disabled, legacy_id, station_status, is_returning) \
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

for entry in clean_data: # for every station entry in the json 
    station_id = int(entry['station_id']) # find and set station_id
    num_ebikes_available = int(entry['num_ebikes_available'])
    num_bikes_available = int(entry['num_bikes_available'])
    is_installed = int(entry['is_installed'])
    last_reported = int(entry['last_reported'])
    num_docks_disabled = int(entry['num_docks_disabled'])
    is_renting = int(entry['is_renting'])
    eightd_has_available_keys = str(entry['eightd_has_available_keys'])
    num_docks_available = int(entry['num_docks_available'])
    num_bikes_disabled = int(entry['num_bikes_disabled'])
    legacy_id = int(entry['legacy_id'])
    station_status = str(entry['station_status'])
    is_returning = int(entry['is_returning'])
                              
        
    query_parameters = (station_id, num_ebikes_available, num_bikes_available, is_installed, last_reported, num_docks_disabled, is_renting, eightd_has_available_keys, num_docks_available, num_bikes_disabled, legacy_id, station_status, is_returning) 
        
    con.execute(query_template, query_parameters)
        
    con.commit()

print("Success!")
