import os
from yaml import load, CLoader as Loader

document = open('./config/predictor.yml', 'r')

config = load(document, Loader=Loader)
config['settings'].setdefault('server', {})
config['settings']['server'].setdefault('port', 8080)
config['settings']['server'].setdefault('metrics_path', '/metrics')

env = {
    'DEBUG_MODE': os.environ.get('DEBUG_MODE', 'INFO').upper(),
    'SAVE_PLOTS': os.environ.get('SAVE_PLOTS', False)
}

def getEnv(key):
    return env[key]

def getSettings(group):
    return config['settings'][group]

def getParams(group_name):
    params = config['params'][group_name]
    params.setdefault('retraining_interval', '1h')
    params.setdefault('training_window', '1h')
    params.setdefault('daily_seasonality', False)
    params.setdefault('weekly_seasonality', False)
    params.setdefault('monthly_seasonality', False)
    params.setdefault('yearly_seasonality', False)
    params.setdefault('seasonality_mode', 'additive')
    params.setdefault('changepoint_prior_scale', 0.05)
    params.setdefault('growth', 'linear')
    params.setdefault('resolution', '15s')
    return params

def getModelTemplate(group_name, template_name):
    template = config['model_templates'][group_name][template_name]
    template['params'] = getParams(template['params'])
    template['group'] = group_name
    template['name'] = template_name
    return template

def getModelTemplates():
    list = []
    for group in config['model_templates']:
        for name in config['model_templates'][group]:
            list.append(getModelTemplate(group, name))
    return list