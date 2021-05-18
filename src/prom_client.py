from config_parser import config
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_timedelta
from datetime import datetime

pc = PrometheusConnect(
    url=config.prometheus.url,
    headers={"Autorization": "bearer "+ config.prometheus.access_token},
    disable_ssl=True,
)

def query(expr, time_range, resolution)
    delta = parse_timedelta("now", time_range)
    return custom_query_range(query: expr, start_time: datetime.now() - delta, end_time: datetime.now(), step: resolution)