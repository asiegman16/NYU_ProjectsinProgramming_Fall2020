

from flask import Flask, render_template, request
from datetime import *

app = Flask(__name__)

import sqlite3
import pandas as pd
from matplotlib.pyplot import *
import matplotlib as plt
matplotlib.use('Agg')

def create_plot(station,con):
    con = sqlite3.connect('citibikeDataForFlask.db') # connect to our database
    user_station_id = request.args.get('station_id')

    df = pd.read_sql("""SELECT station_id,
                    stationName,
                    availableBikes,
                    availableDocks,
                    totalDocks,
                    latitude,
                    longitude,
                    lastCommunicationTime
                FROM StationsData WHERE station_id = (?)""", con=con, params=[user_station_id])

    df['lastCommunicationTime'] = pd.to_datetime(df['lastCommunicationTime'], format='%Y-%m-%d %H:%M:%S %p')

    df['percent_full'] = df['availableBikes']/df['totalDocks']

    df = df[df.lastCommunicationTime != '1969-12-31 07:00:00']

    station_timeseries = df.pivot_table(
                        index='lastCommunicationTime',
                        values='percent_full',
                        aggfunc='mean'
                    ).interpolate(method='time')

    plot = station_timeseries.plot(alpha=.5, figsize=(18, 9), ylim=(0,1), xlim=('2019-10-10 06', '2019-10-10 06:30'))

    filename = 'static/plot-'+str(station)+ '.png'
    fig = plot.get_figure()
    fig.savefig(filename)
    fig.clear()

    return filename


@app.route("/station_status")
def station_status():

    con = sqlite3.connect('citibikeDataForFlask.db') # connect to our database

    user_station_id = request.args.get('station_id')

    con = sqlite3.connect('/Users/siegmanA/Desktop/library_app/citibikeDataForFlask.db') # connect to our db
    cursor = con.cursor()

    # retrieve records of all tables and construct dictionaries for convenient usage at HTML tamplates

    station_data = cursor.execute("SELECT station_id, stationName, availableBikes, lastCommunicationTime FROM StationsData WHERE station_id = ? LIMIT 5", [user_station_id,])

    station_data = [{"station_id": i[0], "stationName": i[1], "availableBikes": i[2], "lastCommunicationTime": i[3]} for i in station_data]

    image_filename = create_plot(user_station_id, con)

    return render_template('citibike.html', user_station_id=user_station_id, image=image_filename, station_data=station_data)

@app.route("/")
def home():
    return render_template('search_stations.html')

@app.route('/search')
def search():

    name = request.args.get('name')

    con = sqlite3.connect('/Users/siegmanA/Desktop/library_app/citibikeDataForFlask.db') # connect to our db
    cursor = con.cursor()

    station_data = cursor.execute("SELECT station_id, stationName, availableBikes, lastCommunicationTime FROM StationsData WHERE availableBikes > ? LIMIT 5", [name,])

    station_data = [{"station_id": i[0], "stationName": i[1], "availableBikes": i[2], "lastCommunicationTime": i[3]} for i in station_data]

    return render_template('citibike.html', name=name, station_data=station_data)





@app.route("/citibike")
def citibike():

    import sqlite3

    con = sqlite3.connect('/Users/siegmanA/Desktop/library_app/citibikeDataForFlask.db') # connect to our db
    cursor = con.cursor()

    # retrieve records of all tables and construct dictionaries for convenient usage at HTML tamplates

    station_data = cursor.execute("SELECT station_id, stationName, availableBikes, lastCommunicationTime FROM StationsData LIMIT 5")

    station_data = [{"station_id": i[0], "stationName": i[1], "availableBikes": i[2], "lastCommunicationTime": i[3]} for i in station_data]

    return render_template('citibike.html', station_data=station_data)

@app.route('/horror')
def horror():

    import requests

    url = 'http://openlibrary.org/subjects/horror.json'

    parameters = {
        'published_in'   : 2000-2010
    }

    resp = requests.get(url, params=parameters)

    data = resp.json()

    titles = set()

    for i in range(0, len(data)):
        title = data['works'][i]['title']
        titles.add(title)

    set_length = len(titles)

    return render_template('horror.html', titles=titles, set_length=set_length)

app.run(host='0.0.0.0', port=5000, debug=True) # anyone can connect, and we're running on port 5000
