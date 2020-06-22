import requests
import pandas as pd
from datetime import datetime as dt
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
from math import sqrt

def get_daily_values():
    end_point = 'https://api.covid19api.com/dayone/country/turkey/status/confirmed'
    daily_confirmed = requests.get(end_point)
    daily_confirmed_json=daily_confirmed.json()
    country_df = pd.DataFrame()
    for i in daily_confirmed_json:
        country_df = country_df.append(
            {
                'timeslot': (dt.strptime(str(i.get('Date')), "%Y-%m-%dT%H:%M:%SZ")).strftime("%Y-%m-%d"),
                'daily_total_case': i.get('Cases'),
            }, ignore_index=True)
    return country_df

def arima_ml(country_df):

    X = country_df['daily_total_case'].values
    size = int(len(X) * 0.80)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(2,1, 0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        # print(output)
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print(obs,yhat[0],obs-yhat[0])
    error = mean_squared_error(test, predictions)
    rmse = sqrt(error)
    print(rmse)
    output = model_fit.forecast(steps=11)

    print(output)
    print(output[0])

    model = ARIMA(X, order=(2, 1, 0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast(steps=11)

    print(output)
    print(output[0])
def run():
    country_df=get_daily_values()
    print(country_df)
    arima_ml(country_df)

run()
