#!/Users/siegmanA/anaconda3/bin/python

import sqlite3

con = sqlite3.connect('/Users/siegmanA/Desktop/NYU_ProjectsinProgramming_Fall2020/(Class 7) Data Visualization/citibikeData2020_Class7.db')

sql = "CREATE TABLE IF NOT EXISTS StationsData (station_id int, num_ebikes_available int, num_bikes_available int, is_installed int, last_reported int, num_docks_disabled int, is_renting int, eightd_has_available_keys varchar(250), num_docks_available int, num_bikes_disabled int, legacy_id int, station_status varchar(250), is_returning int);" 

con.execute(sql)
con.commit()
