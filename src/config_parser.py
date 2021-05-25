from yaml import load, CLoader as Loader

document = open('./config/predictor.yml', 'r')
config = load(document, Loader=Loader)

config['settings'].setdefault('server', {})
config['settings']['server'].setdefault('port', 8080)
config['settings']['server'].setdefault('metrics_path', '/metrics')

def getSettings(group):
    return config['settings'][group]

def getParams(group_name):
    params = config['params'][group_name]
    params.setdefault('training_window', '1h')
    params.setdefault('resolution', '15s')
    params.setdefault('retraining_interval', '1h')    
    params.setdefault('daily_seasonality', False)
    params.setdefault('weekly_seasonality', False)
    params.setdefault('yearly_seasonality', False)
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