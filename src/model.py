import os
from fbprophet import Prophet, serialize
from prometheus_api_client.utils import parse_timedelta
from datetime import datetime, timedelta
import pickle
import pandas as pd
from prom_client import query_range
from scheduler import add_update_job
from util import get_interval_minutes
from config_parser import getEnv
from holiday import get_instance, get_holidays_between
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
            model = PredictorModel.load(metric, self.template)
            logger.info(f'Model {metric["hash"]} loaded from disk')
        except IOError as e:
            model = PredictorModel(metric, self.template)
            logger.info(f'New model {metric["hash"]} created')            

        # Train the model
        model.train()

        # Append the model to the models list
        self.models[model.hash] = model

    def update_model(self, metric):
        model = self.models[metric['hash']]
        model.set_train_df(metric)
        model.train()

class PredictorModel:

    def __init__(self, metric, template):
        self.hash = metric['hash']
        self.template = template
        self.fbmodel = None
        self.forecast = None
        self.train_df = None
        self.set_train_df(metric)

    def get_forecast_minutes(self):
        retraining_interval = self.template['params']['retraining_interval']
        return get_interval_minutes(retraining_interval) * 3

    def set_train_df(self, metric):
        df = pd.DataFrame(metric['values'], columns=['ds', 'y'])
        df['ds'] = pd.to_datetime(arg=df['ds'], origin='unix', unit='s')
        self.train_df = df

    def get_holidays(self):
        if not 'holidays' in self.template:
            return []

        now = datetime.now()
        delta_past = parse_timedelta('now', self.template['params']['training_window'])
        delta_future = timedelta(minutes=self.get_forecast_minutes())

        start_date = now - delta_past
        end_date = now + delta_future

        return get_holidays_between(get_instance(
            self.template['holidays']),
            start_date.date(),
            end_date.date()
        )

    def train(self):
        logger.info(f'Training model {self.hash}...')

        params = self.template['params']
        holidays = pd.DataFrame({
            'holiday': 'holiday',
            'ds': self.get_holidays()
        })

        self.fbmodel = Prophet(
            daily_seasonality = params['daily_seasonality'],
            weekly_seasonality = params['weekly_seasonality'],
            yearly_seasonality = params['yearly_seasonality'],
            seasonality_mode=params['seasonality_mode'],
            changepoint_prior_scale=params['changepoint_prior_scale'],
            growth=params['growth'],
            holidays=holidays
        )

        if params['monthly_seasonality']:
            fourier_order = 5
            if type(params['monthly_seasonality']) == int:
                fourier_order = params['monthly_seasonality']
            self.fbmodel.add_seasonality(name='monthly', period=30.5, fourier_order=fourier_order)

        self.fbmodel.fit(self.train_df)
        self.predict()
        self.save()

    def predict(self):
        df = self.fbmodel.make_future_dataframe(
            periods = self.get_forecast_minutes(),
            freq = '1MIN', 
            include_history = False
        )
        forecast = self.fbmodel.predict(df)
        self.forecast = forecast

    def get_forecast(self, ds):
        forecast = self.forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        forecast = forecast.set_index("ds")
        nearest_index = forecast.index.get_loc(ds, method='nearest')
        return forecast.iloc[[nearest_index]]

    def save(self):
        fbmodel = self.fbmodel
        group_name = self.template['group']
        template_name = self.template['name']
        self.fbmodel = serialize.model_to_json(fbmodel)

        filename = f'{group_name}_{template_name}_{self.hash}'

        # Save the model to disk
        try:
            if not os.path.exists('./config/models'):
                os.makedirs('./config/models')
            with open(f'./config/models/{filename}','wb+') as f:
                pickle.dump(self, f)
        finally:
            self.fbmodel = fbmodel

        # Save the prediction plot to disk
        if getEnv('SAVE_PLOTS'):
            try:
                if not os.path.exists('./config/plots'):
                    os.makedirs('./config/plots')
                self.fbmodel.plot(self.forecast).savefig(f'./config/plots/{filename}.png')
            except Exception:
                pass

    @staticmethod
    def load(metric, template):
        group_name = template['group']
        template_name = template['name']
        hash = metric['hash']
        with open(f'./config/models/{group_name}_{template_name}_{hash}','rb') as f:
            instance = pickle.load(f)
            instance.fbmodel = serialize.model_from_json(instance.fbmodel)
            instance.template = template
            instance.set_train_df(metric)
            return instance
