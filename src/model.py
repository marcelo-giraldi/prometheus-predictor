import json
from fbprophet import Prophet
from prophet.serialize import model_to_json, model_from_json

class PredictorModel:
    metric = None
    template = None
    model = None
    forecast = []

    def __init__(self, metric, template):
        self.metric = metric
        self.template = template
        params = template['params']
        self.model = Prophet(
            daily_seasonality = params.setdefault('daily_seasonality', False),
            weekly_seasonality = params.setdefault('weekly_seasonality', False),
            yearly_seasonality = params.setdefault('yearly_seasonality', False)
        )
    def train(self, df):
        pass
        # also call predict
    def update():
        pass
        # also call predict
    def predict():
        pass
        # updates forecast variable
    def save():
        pass
    def load(self):
        with open('./config/model_serialized_model.json', 'r') as fin:
            self.model = model_from_json(json.load(fin))  # Load model
            # print(md5(json.dumps(obj).encode('utf-8')).hexdigest())
        pass
    def get_forecast(datetime):
        pass
