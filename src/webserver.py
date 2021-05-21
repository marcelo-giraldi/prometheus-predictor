import tornado.web
import tornado.ioloop
from prometheus_api_client import Metric
from prometheus_client import Gauge, generate_latest, REGISTRY
from datetime import datetime, timezone
from controller import model_groups
from config_parser import getSettings

gauges = dict()

class MainHandler(tornado.web.RequestHandler):
    
    async def get(self):
        self.write('Server is up and running')
        self.set_header("Content-Type", "text; charset=utf-8")

class MetricsHandler(tornado.web.RequestHandler):
    
    async def get(self):
        for model_group in model_groups:
            for model in model_group.models:
                metric_name = f'{model.template["name"]}_pred'
                model.metric['metric']['__name__'] = metric_name
                metric = Metric(model.metric)
                if metric_name not in gauges:
                    gauges[metric_name] = Gauge(metric_name, metric_name, {*metric.label_config.keys(), 'value_type'})
                prediction = model.get_forecast(datetime.now(timezone.utc))
                for column in list(prediction.columns):
                    gauges[metric_name].labels(**metric.label_config, value_type=column).set(prediction[column][0])
        self.write(generate_latest(REGISTRY).decode('utf-8'))
        self.set_header("Content-Type", "text; charset=utf-8")

def start():
    settings = getSettings('server')
    app = tornado.web.Application(
        [
            ('/', MainHandler),
            (settings.setdefault('metrics_path', '/metrics'), MetricsHandler),
        ]
    )
    app.listen(settings.setdefault('port', 8080))
    print('Webserver running')
    tornado.ioloop.IOLoop.current().start()