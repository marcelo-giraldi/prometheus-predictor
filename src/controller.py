
models = {}
'''
For each model listed in configuration, check whether it's saved on disk
If not, train the model
Example:
    {
        alertmanager:
            saturation: <model>
            latency: <model>
    }
'''
def load_models():
    '''
    Load models list from configuration
    for each model_template in configuration:
        call model.load(model_template)
        if there is a model:
            append to the models dict
            in parallel, call update_model(model)
        if not:
            in parallel, call train_model(model_template)
            append to the models dict
    '''
    models = {}

def train_model(model_template):
    '''
    time_range = now - training_window
    call df = prom_client.query(expr, time_range)
    model = new Model(model_template)
    model.train(df, params)
    try model.save()
    finally return model
    '''

def update_model(model):
    '''
    time_range = now - retraining_interval_minutes
    call df = prom_client.query(expr, time_range)
    call model.update(df, params)
    try model.save()
    '''