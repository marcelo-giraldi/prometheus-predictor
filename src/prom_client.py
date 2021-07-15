import numpy as np
from util import get_interval_minutes
from config_parser import getSettings
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_timedelta
from datetime import datetime
from hashlib import md5
import json

headers = None
settings = getSettings('prometheus')
if 'access_token' in settings:
    headers = {'Autorization': 'bearer '+ settings['access_token']}

pc = PrometheusConnect(
    url=settings['url'],
    headers=headers,
    disable_ssl=True,
)

def query_range(expr, time_range, resolution, fill_na):
    fill_method = {
        'zeros': fill_na_zeros,
        'default': None
    }[fill_na or 'default']

    delta = parse_timedelta('now', time_range)
    start_time = datetime.now() - delta
    end_time = datetime.now()

    data = pc.custom_query_range(query = expr, start_time=start_time, end_time=end_time, step = resolution)

    if fill_method:
        for item in data:
            item['values'] = fill_method(start_time, end_time, resolution, item['values'])

    return withHash(expr, data)

def query(expr):
    data = pc.custom_query(query = expr)
    return withHash(expr, data)

def getHash(expr, metric):
    return md5(json.dumps({ 'expr': expr, **metric }).encode('utf-8')).hexdigest()

def withHash(expr, data):
    for e in data:
        e['hash'] = getHash(expr, e['metric'])
    return data

def fill_na_zeros(start_time, end_time, resolution, values):
    ts_inicio = round(datetime.timestamp(start_time))
    ts_fim = round(datetime.timestamp(end_time))
    zeros = [[ds, '0'] for ds in np.arange(ts_inicio, ts_fim, get_interval_minutes(resolution) * 60)]
    dict_values = {i[0]:i[1] for i in values}

    for elem in zeros:
        if elem[0] in dict_values:
            elem[1] = dict_values[elem[0]]

    return zeros