import re
import redis
import datetime
import pickle
import time
import json

cache = redis.StrictRedis(
    host = "10.148.0.4",
    port = "6379",
)
    
def collect():
    country_retailers = loads(cache.get('scrapper_time_metrics').decode('utf-8'))
    scrapper_keys = cache.keys('Counter/Scrapper*Total')
    for key in scrapper_keys:
        data = {}
        country_retailer = re.findall(r'Counter/Scrapper(.*?)/Total', str(key))[0]
        count = int(cache.get(key))
        current_time = str(datetime.datetime.now())
        data['count'] = count
        if country_retailer not in country_retailers:
            data['start_time'] = current_time
            data['count'] = count
            data['stop_time'] = None
            country_retailers[country_retailer] = data
            continue
        old_data = country_retailers[country_retailer]
        old_count = old_data['count']
        old_start_time = old_data['start_time']
        old_stop_time = old_data['stop_time']
        if count < old_count:
            data['start_time'] = current_time
            data['stop_time'] = None
        elif old_stop_time == None:
            if count == old_count:
                data['start_time'] = old_start_time
                data['stop_time'] = current_time
        country_retailers[country_retailer] = data
    cache.set('scrapper_time_metrics', json.dumps(country_retailers))
   
    
while(True):
    collect()
    print('YES')
    time.sleep(50)