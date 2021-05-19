from config_parser import config
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_timedelta
from datetime import datetime

headers = None
if config["settings"]["prometheus"]["access_token"]:
    headers = {"Autorization": "bearer "+ config["settings"]["prometheus"]["access_token"]}

pc = PrometheusConnect(
    url=config["settings"]["prometheus_url"],
    headers=headers,
    disable_ssl=True,
)

def query(expr, time_range, resolution):
    delta = parse_timedelta("now", time_range)
    return pc.custom_query_range(query = expr, start_time = datetime.now() - delta, end_time = datetime.now(), step = resolution)
