
from flask import Flask, render_template, json, url_for, request, jsonify,g
import os
import pandas as pd
import json
from datetime import datetime
from datetime import timedelta
from flask_cors import CORS
from flask import Response
from cachetools import TTLCache
import sqlite3
from dateutil import parser
import dateparser

app = Flask(__name__)
CORS(app)
cache = TTLCache(maxsize=100, ttl=300)

DATABASE = 'database.db'  # Specify your database file here

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

conn = sqlite3.connect(database='database.db')


# Function to get a list of available .parquet files from local drive
def get_parquet_files():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data_folder = os.path.join(SITE_ROOT, "static/data")
    parquet_files = [file for file in os.listdir(data_folder) if file.endswith('.parquet')]
    return parquet_files

# Function to get names of available files from database
def get_table_names():
    # conn = sqlite3.connect('database.db')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [row[0] for row in cursor.fetchall()]
    # conn.close()
    return table_names

# Function to get column names from database
def get_all_column_names():
    # conn = sqlite3.connect('database.db')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [row[0] for row in cursor.fetchall()]
    
    all_column_names = set()  # Use a set to store unique column names
    
    for table_name in table_names:
        cursor.execute(f"PRAGMA table_info([{table_name}])")
        
        column_names = [row[1] for row in cursor.fetchall()]
        all_column_names.update(column_names)  # Use update to add unique column names
    
    # conn.close()
    return list(all_column_names)

# Comment if data fetched directly from the local directory
# # # # # # # # # # # # # # # # 
@app.route('/')
def showparquet():
    parquet_files = get_table_names()  # Get the table names from the database
    all_data = get_all_column_names()  # Get all column names from the database
    timeslots = [] # For setting up the time frame for updating graphs

    date = datetime(2023, 8, 23, 5, 0, 0)
    for i in range(24):
        date += timedelta(hours=1)
        timeslots.append(date.strftime('%H:%M'))

    return render_template('graphindex.html', parquet_files=parquet_files, data=all_data, timeslots=timeslots)


def fetch_data(channels, files, sampling_freq):
    all_data = []
    conn = get_db()
    cursor = conn.cursor()
    
    cache_key = (tuple(channels), tuple(files), sampling_freq)
    cached_result = cache.get(cache_key)
    
    if cached_result:
        return cached_result
    try:
        for selected_file in files:
            for channel in channels:
                query = f'SELECT "{channel}",t FROM "{selected_file}";' 
                cursor.execute(query)
                print(f"Executing SQL query: {query}")
                rows = cursor.fetchall()
                for row in range(0, len(rows), sampling_freq):
                    if rows[row][1] is not None:
                        timestamp = parser.parse(rows[row][1]) - timedelta(hours=2)
                        timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                        record = {'timestamp': timestamp, 'channel': channel, 'value': rows[row][0]}
                        all_data.append(record)
        cache[cache_key] = all_data
        return all_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Route to handle the AJAX request and fetch data
@app.route('/fetch_data', methods=['POST'])
def handle_fetch_data():
    request_data = request.get_json()
    selected_channels = request_data.get('channels')
    selected_files = request_data.get('files')
    sampling_freq = request_data.get('sampling_freq')

    print(request_data)
    if not selected_channels or not selected_files:
        return jsonify(error="Invalid request. Please select both channels and files.")

    try:
        data = fetch_data(selected_channels, selected_files, sampling_freq)
        print(data)
        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)