from flask import Flask, jsonify, request
from flask_cors import CORS
from decimal import Decimal
import uuid
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/calculating/<cargo_mass>', methods=['GET'])
def physicalc(cargo_mass):
    cargo_mass = Decimal(cargo_mass)
    m_var = Decimal(cargo_mass + 35000)
    response_object = {'status': 'success'}
    a_var = Decimal(100000 / m_var)
    t_var = Decimal(140 / a_var)
    if (t_var > 60):
        excess_cargo_mass = Decimal(m_var - Decimal(60 * 100000 / 140))
        response_object['calc_result'] = "Take off time is longer than 60 seconds! You have to destroy at least %d kg (out of %d kg)." % (excess_cargo_mass, cargo_mass)
    else:
        x_var = Decimal(a_var * t_var * t_var / 2)
        response_object['calc_result'] = "Take off time is: %d seconds. Take off distance is: %d km." % (t_var, x_var / 1000)
    return jsonify(response_object)

@app.route('/checkWeather', methods=['GET'])
def weather():
    response_tempature_object = {'status': 'success'}
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 30,
        "longitude": 35,
        "start_date": "2023-01-01",
        "end_date": "2023-01-01",
        "hourly": "temperature_2m"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s"),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    tempature_list = hourly_dataframe["temperature_2m"]
    hour_list = hourly_dataframe["date"]
    take_off_hours_list = []
    for i in range(len(tempature_list)):
        if (15 < tempature_list[i] < 30):
            take_off_hours_list.append(hour_list[i])
    if (take_off_hours_list == []):
        response_tempature_object['weather_result'] = "You can't take off! The tempatures are: " + ' degrees Celsius, '.join(map(str, tempature_list)) + ' degrees Celsius.'
    else:
        response_tempature_object['weather_result'] = "Times you can take off: " + toString(take_off_hours_list)
    return jsonify(response_tempature_object)

def toString(timestamps):
    string_timestamps = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in timestamps]
    combined_string = ', '.join(string_timestamps)
    return combined_string

if __name__ == '__main__':
    app.run()