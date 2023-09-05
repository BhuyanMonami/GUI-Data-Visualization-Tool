import pandas as pd
import numpy as np
import os
import argparse
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy import stats
import scipy.spatial as sp, scipy.cluster.hierarchy as hc
import matplotlib.pyplot as plt
import mplcursors 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode, iplot
import plotly.io as pio



def get_parquet_files():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data_folder = os.path.join(SITE_ROOT, "static/data")
    parquet_files = [file for file in os.listdir(data_folder) if file.endswith('.parquet')]
    return parquet_files


# Iterate through each .parquet file and convert to dataframe
def parquet_to_dataframe():
	parquet_files = get_parquet_files()
	all_data = []
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	for parquet_file in parquet_files:
	    file_path = os.path.join(SITE_ROOT, "static/data", parquet_file)
	    print(f"Processing file: {parquet_file}")
	    df = pd.read_parquet(file_path, engine='pyarrow')
	    df['t'] = pd.to_datetime(df['t']).dt.tz_convert(None)
	    all_data.append(df)
	return all_data


# Sanity check to compare with the raw .parquet files

def parquet_to_dataframe_with_column_and_time(file_name, column_names, start_time, end_time):
    dataframes = parquet_to_dataframe()
    
    for i, df in enumerate(dataframes):
        # Extract the date from the file name
        current_file_name = get_parquet_files()[i]
        date_part = current_file_name.split('_')[0]  # Extract the date part from the file name
        target_date = pd.Timestamp(date_part)

        if current_file_name == file_name:
            for column_name in column_names:
                if column_name in df.columns:
                    filtered_df = df[(df['t'].dt.date == target_date.date()) & (df['t'].dt.time >= start_time.time()) & (df['t'].dt.time <= end_time.time())]
            
                    # Check and print the values of the specified column for the filtered timestamps
                    if len(filtered_df) > 0:
                        column_values = filtered_df[column_name]
                        time_values = filtered_df['t']
                        print(f"{column_name} values for timestamps on", target_date, "between", start_time, "and", end_time, ":")
                        for time, value in zip(time_values, column_values):
                            print("Time:", time, f"{column_name}:", value)
                    else:
                        print("No data available for timestamps on", target_date, "between", start_time, "and", end_time)


# Visualization as .html


def generate_interactive_plots(file_name, column_name):
    # Load dataframes from .parquet files using parquet_to_dataframe()
    dataframes = parquet_to_dataframe()

    # Find the dataframe that matches the specified file_name
    matching_dataframe = None
    for df, df_file_name in zip(dataframes, get_parquet_files()):
        if file_name == df_file_name:
            matching_dataframe = df
            break

    if matching_dataframe is not None:
        # Create interactive plot for the specified column
        fig = px.line(matching_dataframe, x='t', y=column_name, title=f'Interactive Plot for {column_name}')

        # Customize the layout if needed
        fig.update_layout(
            xaxis_title='Timestamp',
            yaxis_title=column_name,
            template='plotly_dark',  # You can change the template to your preference
        )

        # Show the interactive plot
        fig.show()
    else:
        print(f"File '{file_name}' not found in the loaded dataframes.")


def generate_plots(file_name, column_names):
    dataframes = parquet_to_dataframe()

    matching_dataframe = None
    for df, df_file_name in zip(dataframes, get_parquet_files()):
        if file_name == df_file_name:
            matching_dataframe = df
            break

    if matching_dataframe is not None:
        data = matching_dataframe.drop(columns=['t', 'hours', 'dt'])
        data.dropna(inplace=True)
        missing_values = data.isnull().sum().sum()
        if missing_values > 0:
            print(f"There are {missing_values} missing values in the DataFrame.")
        else:
            print("There are no missing values in the DataFrame.")

        infinite_values = np.any(~np.isfinite(data))
        if infinite_values:
            print("The DataFrame contains at least one infinite value.")
        else:
            print("The DataFrame does not contain any infinite values.")

        column_variances_data = data.var()
        zero_variance_features_data = column_variances_data[column_variances_data == 0].index
        num_zero_variance_features_data = len(zero_variance_features_data)
        print(data.columns[data.var() == 0])

        if num_zero_variance_features_data > 0:
            print(f"Number of features with zero variance: {num_zero_variance_features_data}")
            # print(f"Features with zero variance: {', '.join(zero_variance_features_data)}")
        else:
            print("No features with zero variance found.")

        # Normalise the channels
        # scaler = StandardScaler()
        data_normalized = data
        # data_normalized = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
        # print(data_normalized.columns[data.var() == 0]) #check the number of columns with zero variance
        column_variances_data = data_normalized.var()
        zero_variance_features_data = column_variances_data[column_variances_data == 0].index
        data_normalized.drop(zero_variance_features_data, axis=1, inplace=True) # Drop columns with zero variance
        print("\nDataFrame after removing columns with zero variance:")
        print(data_normalized.shape)
        corr_matrix = data_normalized.corr()
        corr_table = pd.DataFrame(corr_matrix)

        # Save correlation table
        save_dir = os.path.join('static', 'data', 'data_heatmaps', file_name)
        os.makedirs(save_dir, exist_ok=True)
        correlation_table_file = os.path.join(save_dir, f'correlation_table_{file_name[:-8]}.csv')
        corr_table.to_csv(correlation_table_file, index=True)
        print(f"Correlation table saved as {correlation_table_file}")

        # Create the interactive cluster heatmap using Plotly
        fig_heatmap = create_heatmap(corr_matrix, file_name)
        heatmap_file = os.path.join(save_dir, f'correlation_heatmap_{file_name[:-8]}.html')

        # Save the interactive cluster heatmap as an HTML file
        fig_heatmap.write_html(heatmap_file)
        print(f"Correlation Heatmap saved as {heatmap_file}")

        # Create and save distribution plot,box plot
        distribution(data_normalized, file_name, column_names)
        analyze_data_with_iqr(data_normalized, file_name, column_names)


# FUNCTION TO CREATE CORRELATION HEATMAP
def create_heatmap(data_normalized, file_name):
    fig = go.Figure(data=go.Heatmap(
        z=data_normalized.corr(),
        x=data_normalized.columns,
        y=data_normalized.columns,
        colorscale='Viridis'
    ))
    fig.update_layout(
        title=f"Correlation Heatmap for {file_name}",
        xaxis_title="Features",
        yaxis_title="Features"
    )
    return fig

# FUNCTION TO CHECK THE DISTRIBUTION FOR A SELECTED CHANNEL USING A HISTOGRAM
def distribution(data_normalized, file_name, column_names):
    # Set the theme
    sns.set_theme()

    for column_name in column_names:
        save_dir = os.path.join('static', 'data', 'data_anomalies','distribution_plots', file_name, column_name)
        os.makedirs(save_dir, exist_ok=True)
        
        # Create a distribution plot for the specified column
        plot = sns.displot(data_normalized[column_name])
        plot.set(
            title=f"Distribution of {column_name}",
            xlabel=column_name
        )
        

        # Save the distribution plot as an image file
        distribution_image_file = os.path.join(save_dir, f'distribution_{file_name[:-8]}_{column_name}.png')
        plot.savefig(distribution_image_file)
        # Show the plot
        plt.show()
        print(f"Distribution plot for {column_name} saved as {distribution_image_file}")


# FUNCTION TO IDENTIFY OUTLIERS USING IQR METHOD

def detect_outliers_iqr(data):
    outliers = []
    data = sorted(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    IQR = q3 - q1
    lower_bound = q1 - (1.5 * IQR)
    upper_bound = q3 + (1.5 * IQR)
    for i in data:
        if i < lower_bound or i > upper_bound:
            outliers.append(i)
    return outliers


def analyze_data_with_iqr(data_normalized, file_name, column_names):
    for column_name in column_names:
        save_dir = os.path.join('static', 'data', 'data_anomalies', 'box_plots', file_name, column_name)
        os.makedirs(save_dir, exist_ok=True)
        sorted_data = data_normalized[column_name].sort_values()
        analyzed_data = sorted_data.describe()
        
        # Create a new figure and axis for the boxplot
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create the boxplot and set labels
        sns.boxplot(data=sorted_data, orient='v', ax=ax)
        ax.set_xlabel(column_name)
        ax.text(0.6, 0.9, f"Total Data Points: {analyzed_data['count']:.0f}", transform=ax.transAxes, fontsize=5)
        ax.text(0.6, 0.85, f"Num Outliers: {len(detect_outliers_iqr(data_normalized[column_name]))}", transform=ax.transAxes, fontsize=5)

        pd.set_option('display.max_colwidth', None)
        
        # Convert the analyzed data to a string
        analyzed_data_str = analyzed_data.to_string()

        pd.reset_option('display.max_colwidth')
        
        # Add the analyzed data as text annotations
        ax.text(0.85, 0.9, analyzed_data_str, transform=ax.transAxes, fontsize=5, va='center')
        
        # Set the title for the figure
        plt.title(f"Boxplot and Analyzed Data for {column_name}")
        
        # Save the figure as an HTML file
        boxplot_file = os.path.join(save_dir, f'boxplot_{file_name[:-8]}_{column_name}.png')
        fig.savefig(boxplot_file)
        print(f"Boxplot saved as {boxplot_file}")
        
        # Show the plot
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Perform data analysis on parquet files.")
    parser.add_argument("--start-time", required=True, type=str, help="Start time in HH:MM:SS format")
    parser.add_argument("--end-time", required=True, type=str, help="End time in HH:MM:SS format")
    parser.add_argument("--file-name", required=True, type=str, help="Name of the parquet file")
    parser.add_argument("--column-names", required=True, nargs='+', type=str, help="Column names to analyze")

    args = parser.parse_args()

    start_time = pd.Timestamp(args.start_time)
    end_time = pd.Timestamp(args.end_time)
    file_name = args.file_name
    column_names = args.column_names

    # Call your functions with the provided arguments here
    
    generate_plots(file_name, column_names)
    parquet_to_dataframe_with_column_and_time(file_name, column_names, start_time, end_time)

if __name__ == "__main__":
    main()
           

