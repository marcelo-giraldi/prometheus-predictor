from copy import deepcopy
from yaml import load, CLoader as Loader

document = open('./config/predictor.yml', 'r')
config = load(document, Loader=Loader)

def getSettings(group):
    return deepcopy(config['settings'][group])

def getParams(group_name):
    return deepcopy(config['params'][group_name])

def getModelTemplate(group_name, template_name):
    template = deepcopy(config['model_templates'][group_name][template_name])
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