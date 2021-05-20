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

def query_range(expr, time_range, resolution):
    delta = parse_timedelta('now', time_range)
    data = pc.custom_query_range(query = expr, start_time = datetime.now() - delta, end_time = datetime.now(), step = resolution)
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
