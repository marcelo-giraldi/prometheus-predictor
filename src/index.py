import controller, webserver, scheduler
import logging

logging.basicConfig(level=logging.DEBUG)

logging.info('Starting scheduler...')
scheduler.start()

logging.info('Starting controller...')
controller.start()

logging.info('Starting webserver...')
webserver.start()
