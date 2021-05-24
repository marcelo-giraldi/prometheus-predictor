import schedule
import time
from threading import Thread
from util import get_interval_minutes

def addJob(model_group):
    params = model_group.template['params']
    interval = params.setdefault('retraining_interval', '1h')
    schedule.every(get_interval_minutes(interval)).minutes.do(model_group.update_models)

def start():
    thread = Thread(target=run, args=())
    thread.start()

def run():
    while True:
        schedule.run_pending()
        time.sleep(1)
