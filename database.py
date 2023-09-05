import pandas as pd
import sqlite3
import os


def get_parquet_files():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data_folder = os.path.join(SITE_ROOT, "static/data")
    parquet_files = [file for file in os.listdir(data_folder) if file.endswith('.parquet')]
    return parquet_files

db_conn = sqlite3.connect(database='database.db')
parquet_files = get_parquet_files()
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
for index, parquet_file in enumerate(parquet_files):
	parquet_file_path = os.path.join(SITE_ROOT, "static/data", parquet_file)
	df_parquet = pd.read_parquet(parquet_file_path, engine='pyarrow')
	table_name= parquet_file .split('.')[0]
	num_rows_inserted = df_parquet.to_sql(table_name,db_conn,index=False)



