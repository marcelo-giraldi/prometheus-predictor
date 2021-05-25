# How to configure prometheus-predictor

In order to use prometheus-predictor in Production, you need to overwrite the YAML file *predictor.yml* in the /opt/pp/config directory. Otherwise, it will run in a *demo mode*:

```
Dockerfile:

[...]
WORKDIR /opt/pp
ADD predictor.yml config/predictor.yml
```

## predictor.yml syntax
The predictor.yml file has the following sintax: 

```
settings:
  # How to connect to the Prometheus server
  prometheus:
    url: <string>
    [access_token: <string>]
  # Local webserver configuration
  [server:]
    [port: <integer> | default = 8080]
    [metrics_path: <string> | default = /metrics]


params:
  # You can define one or more param groups. Each model reference a group name to define its params
  <params_group_name>:
    # How often the model will get new data and retrain
    [retraining_interval: <interval> | default = 1h]

    # How much time of data will be used to train the model
    [training_window: <interval> | default = 7d]

    # You can just set a seasonality True or False, or assign it a fourier order
    # More info: https://facebook.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html#fourier-order-for-seasonalities
    [daily_seasonality: <bool|integer> | default: False]
    [weekly_seasonality: <bool|integer> | default: False]
    [monthly_seasonality: <bool|integer> | default: False]
    [yearly_seasonality: <bool|integer> | default: False]

    # How the seasonality will affect the trend. 
    # More info: https://facebook.github.io/prophet/docs/multiplicative_seasonality.html
    [seasonality_mode: <string> | default: 'additive']

    # How flexible is the trend
    # Mode info: https://facebook.github.io/prophet/docs/trend_changepoints.html
    [changepoint_prior_scale: <float> | default: 0.05]

    # How the forecast will grow
    # More info: https://facebook.github.io/prophet/docs/saturating_forecasts.html#forecasting-growth
    [growth: <string> | default: 'linear']

    # The precision of the query result
    [resolution: <interval> | default: 15s]

model_templates:
  # You can define one or more model template groups. Each group has one or more model templates
  # Each model template defines the setup for a prediction model
  <template_group_name>:
    <model_template_name>:
      # PromQL expression to get data
      expr: <PromQL expression>

      # Params group name associated to this model template
      params: <params_group_name>
```