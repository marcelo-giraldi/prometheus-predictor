from copy import deepcopy
from yaml import load, CLoader as Loader
from util import setDefault

document = open('./config/predictor.yml', 'r')
config = load(document, Loader=Loader)

def getSettings():
    return deepcopy(config['settings'])

def getParams(group_name):
    params = deepcopy(config['params'][group_name])
    setDefault(params, 'retraining_interval', '1h')
    setDefault(params, 'training_window', '7d')
    setDefault(params, 'daily_seasonality', False)
    setDefault(params, 'weekly_seasonality', False)
    setDefault(params, 'yearly_seasonality', False)
    setDefault(params, 'resolution', '15s')
    return params

def getModelTemplate(group_name, template_name):
    template = deepcopy(config['model_templates'][group_name][template_name])
    template['params'] = getParams(template['params'])
    return template
