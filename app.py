
from flask import Flask, render_template, json, url_for, request, jsonify
import os
import pandas as pd
import json
from datetime import datetime
from datetime import timedelta
from flask_cors import CORS
from flask import Response
from cachetools import TTLCache

app = Flask(__name__)
CORS(app)
cache = TTLCache(maxsize=100, ttl=300)

# Function to get a list of available .parquet files
def get_parquet_files():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data_folder = os.path.join(SITE_ROOT, "static/data")
    parquet_files = [file for file in os.listdir(data_folder) if file.endswith('.parquet')]
    return parquet_files

# Route for the home page (index.html)
@app.route('/')
def showparquet():
    parquet_files = get_parquet_files()
    all_data = []
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    for index, parquet_file in enumerate(parquet_files):
        parquet_file_path = os.path.join(SITE_ROOT, "static/data", parquet_file)
        data = pd.read_parquet(parquet_file_path, engine='pyarrow')
        data['t'] = pd.to_datetime(data['t']).dt.tz_convert(None)
        a = data.columns.values.tolist()
        for column_name in a:
            if not column_name in all_data:
                all_data.append(column_name)

    timeslots = []
    date = datetime(2023,8,23,5,0,0)
    for i in range(24):
        date += timedelta(hours=1)
        timeslots.append(date.strftime('%H:%M'))

    return render_template('graphindex.html', parquet_files=parquet_files, data=all_data, timeslots=timeslots)


def fetch_data(channels, files):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    all_data = []
    cache_key = (tuple(channels), tuple(files))
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    for selected_file in files:
        parquet_file_path = os.path.join(SITE_ROOT, "static/data", selected_file)
        data = pd.read_parquet(parquet_file_path, engine='pyarrow')
        data['t'] = pd.to_datetime(data['t']).dt.tz_convert(None)
        data['t'] =data['t'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        selected_file_data = []
        for channel in channels:
            if channel in data.columns:
                channel_data = data[channel].tolist()
                for timestamp, value in zip(data['t'], channel_data):
                    record = {'timestamp': timestamp, 'channel': channel, 'value': value}
                    selected_file_data.append(record)

        # Filter out records with NaN values
        selected_file_data = [record for record in selected_file_data if not pd.isna(record['value'])]
        all_data.extend(selected_file_data)
    cache[cache_key] = all_data
    all_data_new = [all_data[x] for x in range(0, len(all_data), 60)]
    return all_data_new


# Route to handle the AJAX request and fetch data
@app.route('/fetch_data', methods=['POST'])
def handle_fetch_data():
    request_data = request.get_json()
    selected_channels = request_data.get('channels')
    selected_files = request_data.get('files')

    print(request_data)
    if not selected_channels or not selected_files:
        return jsonify(error="Invalid request. Please select both channels and files.")

    try:
        data = fetch_data(selected_channels, selected_files)
        print(data)
        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e))







if __name__ == '__main__':
    app.run(debug=True)


