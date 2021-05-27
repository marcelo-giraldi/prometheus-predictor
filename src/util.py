from datetime import timedelta
from prometheus_api_client.utils import parse_timedelta

def get_interval_minutes(interval):
    delta = parse_timedelta('now', interval)
    return round(delta.seconds / 60)

def get_formatted_metric(name, labels, value):
    formatted_labels = []
    if not labels:
        return f'{name} {value}'
    if '__name__' in labels:
        labels.pop('__name__')
    for label_name in labels:
        formatted_labels.append(f'{label_name}="{labels[label_name]}"')
    return f'{name}{{{",".join(formatted_labels)}}} {value}'

def date_range(start_date, end_date, exclusive=True):
    if not exclusive:
        end_date = end_date + timedelta(days=1)
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)