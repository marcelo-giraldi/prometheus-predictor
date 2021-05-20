from config_parser import getSettings
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_timedelta
from datetime import datetime

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
    return pc.custom_query_range(query = expr, start_time = datetime.now() - delta, end_time = datetime.now(), step = resolution)

def query(expr):
    return pc.custom_query(query = expr)
