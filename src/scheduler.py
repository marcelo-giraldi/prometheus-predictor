import schedule
import time
from threading import Thread
from util import get_interval_minutes
import logging

logger = logging.getLogger(__name__)

def add_update_job(model_group):
    params = model_group.template['params']
    interval_minutes = get_interval_minutes(params['retraining_interval'])
    logger.info(f'Scheduling retraining for model group {model_group.id} every {interval_minutes} minutes...')
    schedule.every(interval_minutes).minutes.do(model_group.update_models)

def update_all_now():
    schedule.run_all()

def start():
    thread = Thread(target=run, args=(), daemon=True)
    thread.start()

def run():
    while True:
        schedule.run_pending()
        time.sleep(1)
