import sys
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
