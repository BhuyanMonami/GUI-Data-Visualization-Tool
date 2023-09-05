import os
import pandas as pd

# Path to the directory containing all .parquet files
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# List all .parquet files in the directory
data_folder = os.path.join(SITE_ROOT, "static/data")
parquet_files = [file for file in os.listdir(data_folder) if file.endswith('.parquet')]
missing_values_info = []
zero_variance_info = {'File Name': []}
# Set to store unique 'Column' names with missing data in each file


# Iterate through each .parquet file
for parquet_file in parquet_files:
    file_path = os.path.join(SITE_ROOT, "static/data", parquet_file)
    print(f"Processing file: {parquet_file}")
    
    # Read the .parquet file into a DataFrame
    df = pd.read_parquet(file_path, engine='pyarrow')
    df['t'] = pd.to_datetime(df['t']).dt.tz_convert(None)
    data = df.drop(columns=['t', 'hours', 'dt'])
    
    # Find missing values and their locations
    missing_values = data.isnull()
    
    if missing_values.any().any():
        print(f"Missing values found in file: {parquet_file}")
        total_missing_values = missing_values.sum().sum()
        print(f"Total missing values in {parquet_file}: {total_missing_values}")

        # Update the set of unique 'Column' names with missing data in this file
     
        
        # Iterate through each column to find missing values
        for column in data.columns:
            column_missing_values = missing_values[column]
            if column_missing_values.any():
                # Get the row numbers where missing values are present
                rows_with_missing = column_missing_values[column_missing_values].index.tolist()
                print(f"Column: {column}, Missing in Rows: {rows_with_missing}")
                missing_values_info.append({
                    'File name': parquet_file,
                    'Column': column,
                    'Missing Rows': rows_with_missing
                })
    else:
        print("No missing values found in file.\n")

    column_variances = data.var()
    zero_variance_columns = column_variances[column_variances == 0].index
    num_zero_variance_columns = len(zero_variance_columns)
    
    if num_zero_variance_columns > 0:
        print(f"Number of features with zero variance in {parquet_file}: {num_zero_variance_columns}")
        print(f"Features with zero variance in {parquet_file}: {', '.join(zero_variance_columns)}")
    else:
        print(f"No features with zero variance found in {parquet_file}.\n")
    
    for column in data.columns:
        if column in zero_variance_columns:
            zero_variance_info.setdefault(column, []).append(0)
        else:
            zero_variance_info.setdefault(column, []).append(1)
    zero_variance_info['File Name'].append(parquet_file)


missing_values_df = pd.DataFrame(missing_values_info)
zero_variance_df = pd.DataFrame(zero_variance_info)

print(missing_values_df)
print(zero_variance_df)
print("Processing of all files completed.")

# Convert the DataFrames to CSV and save it to a file
csv_file_path = os.path.join(SITE_ROOT, "static/data/data_anomalies", "missing_values.csv")
zero_variance_csv_path = os.path.join(SITE_ROOT, "static/data/data_anomalies", "zero_variance_features.csv")
missing_values_df.to_csv(csv_file_path, index=False)
zero_variance_df.to_csv(zero_variance_csv_path, index=False)

print("Missing values DataFrame saved to CSV.")



