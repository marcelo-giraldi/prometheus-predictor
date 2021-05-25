from threading import Thread
from model import PredictorModelGroup
from config_parser import getModelTemplates
from scheduler import update_all_now
import logging

logger = logging.getLogger(__name__)

model_groups = []

def start(): 
    thread = Thread(target=load_models, args=(), daemon=True)
    thread.start()

def load_models():
    logger.info('Loading models from templates...')
    for template in getModelTemplates():
        model_group = PredictorModelGroup(template)
        model_groups.append(model_group)
        model_group.load_models()
    logger.info('Models loaded. Updating all...')
    update_all_now()
