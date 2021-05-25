import logging
import controller, webserver, scheduler
from config_parser import getEnv

LOGLEVEL = getEnv('DEBUG_MODE')
logging.basicConfig(level=LOGLEVEL)

logging.info('Starting scheduler...')
scheduler.start()

logging.info('Starting controller...')
controller.start()

logging.info('Starting webserver...')
webserver.start()
