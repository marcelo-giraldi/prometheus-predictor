from yaml import load, CLoader as Loader

document = open('./config/predictor.yml', 'r')
config = load(document, Loader=Loader)