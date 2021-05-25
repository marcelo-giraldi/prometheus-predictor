import os
import logging
import controller, webserver, scheduler

LOGLEVEL = os.environ.get('DEBUG_MODE', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

logging.info('Starting scheduler...')
scheduler.start()

logging.info('Starting controller...')
controller.start()

logging.info('Starting webserver...')
webserver.start()
