import tornado.web
import tornado.ioloop
from datetime import datetime, timezone
from controller import model_groups
from config_parser import getSettings
from util import get_formatted_metric
import logging

logger = logging.getLogger(__name__)

class MainHandler(tornado.web.RequestHandler):
    
    async def get(self):
        self.write('Server is up and running')
        self.set_header("Content-Type", "text; charset=utf-8")

class MetricsHandler(tornado.web.RequestHandler):

    async def get(self):
        self.metrics_list = []

        for model_group in model_groups:
            for model in model_group.models.values():
                self.set_metrics(model)

        self.write('\n'.join(self.metrics_list))
        self.set_header("Content-Type", "text; charset=utf-8")

    def set_metrics(self, model):
        metric_name = f'{model.template["name"]}_pred'
        labels = model.metric['metric']
        prediction = model.get_forecast(datetime.now(timezone.utc))

        for column in list(prediction.columns):
            self.metrics_list.append(get_formatted_metric(metric_name, labels, prediction[column][0]))

def start():
    settings = getSettings('server')
    app = tornado.web.Application(
        [
            ('/', MainHandler),
            (settings.setdefault('metrics_path', '/metrics'), MetricsHandler),
        ]
    )
    app.listen(settings.setdefault('port', 8080))
    tornado.ioloop.IOLoop.current().start()