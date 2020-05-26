from flask import Flask, render_template
import feedparser
import random
import time
from datetime import datetime, timezone
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *

matplotlib.use('Agg')

app = Flask(__name__)

def create_plot():


    wired_url = "https://www.wired.com/feed/rss"
    wired_feed = feedparser.parse(wired_url)

    article_data = [{"title": wired_feed['entries'][i]['title'], "summary": wired_feed['entries'][i]['summary'], "published": pd.to_datetime(wired_feed['entries'][i]['published'])} for i in range(0,len(wired_feed))]

    title_length_list = []

    for i in article_data:
        title = i['title']
        title_length = len(title)
        title_length_list.append(title_length)

    df = pd.DataFrame(title_length_list)

    fig = plt.hist(title_length_list, bins=5)

    plt.title('Wired Article Title Length')
    plt.xlabel("Length (In Characters)")
    plt.ylabel("Frequency")
    plt.savefig("abc.png")

    filename = 'static/plot-'+str(datetime.now(timezone.utc))+ '.png'
    plt.savefig(filename)

    return filename

@app.route('/')
def home():

    wired_url = "https://www.wired.com/feed/rss"
    wired_feed = feedparser.parse(wired_url)

    article_data = [{"title": wired_feed['entries'][i]['title'], "summary": wired_feed['entries'][i]['summary'], "published": pd.to_datetime(wired_feed['entries'][i]['published'])} for i in range(0,len(wired_feed))]

    now = datetime.now(timezone.utc)

    hours = now + timedelta(hours=-1)

    image_filename = create_plot()

    return render_template("wired.html", article_data=article_data, now=now, hours=hours, image=image_filename)

app.run(host='0.0.0.0', port=5000, debug=True) # anyone can connect, and we're running on port 5000
