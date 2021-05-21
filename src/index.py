import controller, webserver, scheduler
from threading import Thread

ctrl = Thread(target=controller.load_models, args=())
ctrl.start()
webserver.start()
# scheduler.schedule()
