from flask import Flask
from flask import request
from json import dumps,loads
from random import randint
from flask import jsonify
import re
from flask import Markup
import markdown
from flask import render_template
import redis
import datetime
from datetime import timedelta
import pickle
import threading

#country_retailers_pickle_path = '/usr/src/app/web/static/country_retailers.p'

app = Flask(__name__)

cache = redis.StrictRedis(
    host = "10.148.0.4",
    port = "6379",
)
    
def help_decorator(f):
    """
    Returns the function info
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "/help" in request.path:
            return f.__doc__
        return f(*args, **kwargs)
    return decorated_function

app.debug = True

@app.route('/')
def times():
    country_retailers = loads(cache.get('scrapper_time_metrics').decode('utf-8'))
    data = []
    for cr_key in country_retailers:
        country_retailer = country_retailers[cr_key]
        start_time = datetime.datetime.strptime(country_retailer['start_time'], "%Y-%m-%d %H:%M:%S.%f")
        stop_time = country_retailer.get('stop_time', None)          
        error = country_retailer.get('error', None)
        cr_data = {}   
        cr_data['key'] = cr_key
        cr_data['date'] = str(start_time.date())
        cr_data['start_time'] = str(start_time.time())
        if stop_time:
            stop_time = datetime.datetime.strptime(country_retailer['stop_time'], "%Y-%m-%d %H:%M:%S.%f")
            cr_data['stop_time'] = str(stop_time.time())
            cr_data['duration'] = str(stop_time - start_time)
        if error:
            cr_data['duration'] = error
        data.append(cr_data)
    return render_template('index.html', **locals())
