from prometheus_api_client.utils import parse_timedelta

def get_interval_minutes(interval):
    delta = parse_timedelta('now', interval)
    return int(delta.seconds / 60) * 3

def get_formatted_metric(name, labels, value):
    formatted_labels = []
    if not labels:
        return f'{name} {value}'
    if '__name__' in labels:
        labels.pop('__name__')
    for label_name in labels:
        formatted_labels.append(f'{label_name}="{labels[label_name]}"')
    return f'{name}{{{",".join(formatted_labels)}}} {value}'
