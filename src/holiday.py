import sys
from util import date_range
import pandas as pd

sys.path.insert(1, './config')

def get_instance(config):
    Holidays = None
    if config['mode'] == 'default':
        import holidays
        Holidays = getattr(holidays, config['class_name'])
    elif config['mode'] == 'custom':
        import custom_holidays
        Holidays = getattr(custom_holidays, config['class_name'])
    return Holidays()

def get_holidays_between(instance, start_date, end_date):
    holidays = []

    for date in date_range(start_date, end_date, exclusive=False):
        if date in instance:
            holiday_names = instance.get(date).split(', ')
            for holiday_name in holiday_names:
                holidays.append([holiday_name, date])

    return pd.DataFrame(holidays, columns=['holiday', 'ds'])