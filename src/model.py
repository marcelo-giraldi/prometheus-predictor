from fbprophet import Prophet, serialize
import pickle
import pandas as pd
from prom_client import query_range
from scheduler import add_update_job
from util import get_interval_minutes
import logging

logger = logging.getLogger(__name__)

class PredictorModelGroup:

    def __init__(self, template):
        self.template = template
        self.models = {}
        self.id = f'{template["group"]}-{template["name"]}'

    def load_models(self):
        self.load_data(self.load_model)
        add_update_job(self)
    
    def update_models(self):
        self.load_data(self.update_model)

    def load_data(self, callback):
        # Get the data from Prometheus for the given expression
        logger.info(f'Loading data from Prometheus for model group {self.id}...')
        metrics = query_range(
            self.template['expr'],
            self.template['params']['training_window'], 
            self.template['params']['resolution']
        )

        if callback:
            for metric in metrics:
                callback(metric)
        
        return metrics
    
    def load_model(self, metric):
        # Try to load a model instance from disk. If there is none, creates a new instance
        try:
            model = PredictorModel.load(self.template['group'], self.template['name'], metric['hash'])
        except IOError as e:
            model = PredictorModel(metric, self.template)
            model.train()

        # Append the model to the models list
        self.models[model.metric['hash']] = model

    def update_model(self, metric):
        model = self.models[metric['hash']]
        model.update(metric)

class PredictorModel:

    def __init__(self, metric, template):
        self.metric = metric
        self.template = template
        self.fbmodel = None
        self.forecast = None

    def train(self):
        logger.info(f'Training model {self.metric["hash"]}...')

        params = self.template['params']
        self.fbmodel = Prophet(
            daily_seasonality = params['daily_seasonality'],
            weekly_seasonality = params['weekly_seasonality'],
            yearly_seasonality = params['yearly_seasonality']
        )

        df = pd.DataFrame(self.metric['values'], columns=['ds', 'y'])
        df['ds'] = pd.to_datetime(arg=df['ds'], origin='unix', unit='s')

        self.fbmodel.fit(df)
        self.predict()
        self.save()

    def update(self, metric):
        logger.info(f'Updating model {self.metric["hash"]}...')
        self.metric = metric
        self.train()

    def predict(self):
        retraining_interval = self.template['params']['retraining_interval']
        prediction_interval_minutes = get_interval_minutes(retraining_interval) * 3
        df = self.fbmodel.make_future_dataframe(
            periods = prediction_interval_minutes, 
            freq = '1MIN', 
            include_history = False
        )
        forecast = self.fbmodel.predict(df)
        forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        forecast = forecast.set_index("ds")
        self.forecast = forecast

    def get_forecast(self, ds):
        nearest_index = self.forecast.index.get_loc(ds, method='nearest')
        return self.forecast.iloc[[nearest_index]]

    def save(self):
        fbmodel = self.fbmodel
        group_name = self.template['group']
        template_name = self.template['name']
        self.fbmodel = serialize.model_to_json(fbmodel)
        try:
            with open(f'./config/models/{group_name}_{template_name}_{self.metric["hash"]}','wb+') as f:
                pickle.dump(self, f)
        finally:
            self.fbmodel = fbmodel

    @staticmethod
    def load(group_name, template_name, hash):
        with open(f'./config/models/{group_name}_{template_name}_{hash}','rb') as f:
            instance = pickle.load(f)
            instance.fbmodel = serialize.model_from_json(instance.fbmodel)
            return instance
