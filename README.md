# GUI Visualization Tool for First Hydrogen Vehicle Channel Data

## Description

This GUI application is designed to provide a user-friendly interface for visualizing and analyzing data from the First Hydrogen Prototype Vehicle Channel data. It aims to simplify the process of exploring and understanding the data collected from the hydrogen vehicles. 


**Development Stage:** In its current state, this GUI tool is actively under development. 
- **Backend:** The server-side code is written in Python using Flask.
- **Frontend:** The user interface is built with HTML and JavaScript.
 We are continuously working on improving its features, stability, and user experience.

**Local Development:**
- To develop the application locally, you can use this repository's codebase.
- Start the development server from Python using the `Flask.run()` method. This will launch the server at http://localhost:5000/.


## Installation
### Step 1: Install Python 3.9 or Newer

Before you can run this application locally, ensure you have Python 3.8 or a newer version installed on your system. Follow the appropriate instructions below based on your operating system:

#### Windows:

1. Visit the [Python Downloads](https://www.python.org/downloads/) page.
2. Download the latest Python installer for Windows.
3. Run the installer.
4. During installation, be sure to check the box that says "Add Python X.X to PATH" (X.X represents your Python version).
5. Complete the installation.

#### Linux (Ubuntu/Debian):

Open a terminal and enter the following commands:

```
sudo apt update
sudo apt install python3.11
```

To verify your installation, open a terminal and run:

```
python --version
```
### Step 2: Clone this Repository
To work with this application locally, you need to clone this repository to your machine.
1. Change the current working directory to the location where you want the cloned directory.
2. Open a terminal or command prompt and use the following commands:
   ```
   git clone https://github.com/MonamiBhuyan/FirstHydrogenGUI.git
   ```
### Step 3: Install Virtual Environment
1. Install `virtualenv`:
   ```
   $ pip install virtualenv
   ```
2. Open a terminal in the project root directory (FirstHydrogenGUI)and run:
   ```
   $ virtualenv FH
   ```
3. Then run the command:
   ```
   $ .\FH\Scripts\activate
   ```
### Step 4: Install Flask and Dependencies 
1. Install Flask and SQLAlchemy:
   ```
   $ (FH) pip install flask flask-sqlalchemy
   ```
   
## How to Run
1. Finally start the web server:
   ```
   $ (FH) python app.py
   ```
This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```

## Static files and Database

1. The code graphindex.html has provision for fetching data from both the local directory as well as an SQL database. 
2. Run the following code to add the .parquet files to the database after storing the files in the "static/data" directory:
   ```
   $ (FH) python database.py
   ```

3. If you want to add more files to the database, then you can do so by first storing the files in the "static/data" directory and then modifying the code for `database.py` in the following way:
```
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
   table_name = parquet_file.split('.')[0]
   num_rows_inserted = df_parquet.to_sql(table_name, db_conn, index=False)
```

This code will detect the new .parquet files in the "static/data" folder and insert them into the SQLite database as new tables while keeping the existing ones intact.

4. If you wish to fetch the data from the local directory instead, then simply uncomment the relevant code from `app.py` and run the code as usual. However, it is recommended to maintain a database in SQL server for better managing and analyzing of data as well as to keep data secure.

5. If there are files from different vehicles, then the .parquet files should be named with a vehicle identifier and then they can be stored in the same "static/data" folder. All the other functionalities would be the same. Minor adjustments might be needed in the front end JS code(`app.js`)

6. The database is currently saved as 'database.db' in the same directory where our Python script is located. In order to make it accessible to clients, the database (in our case, 'database.db') should be hosted on a server. This server can be a cloud-based server, a dedicated hosting server, or a server within your organization's network(like Cambridge). The database server should be accessible to both your web application and the clients via a network connection.

## Hosting the code in Cambridge platform

The goal is to host the GUI platform in First Hydrogen's dedicated Cambridge platform at https://hydrogen-vans.srcp.hpc.cam.ac.uk 

We are seeking assistance from the concerned IT personnel to help us with this step. This section of the documentation shall be updated once the GUI platform is migrated to this dedicated Cambridge environment.

## Further Optimization

The GUI platform needs to be tested under various conditions to find edge cases. It is to be noted that while it allows the user to choose the frequency at which data points are collected for rendering the graph, as one decreases the frequency, the platoform becomes considerably slower. Further optimization of the code is needed in future development satges to address perdormance and memory issues.

## Access

1. Our Flask application will listen on all available network interfaces on your machine. In practical terms, it makes your application accessible from any device that can reach your machine over the network, including other devices on your local network and potentially over the internet (depending on your network and firewall settings).

2. You run `python app.py` on your machine, which starts the Flask development server and makes your web application accessible locally at http://localhost:5000/.

3. Other users on the same network can access your web application by using your machine's IP address and the port on which the Flask server is running. For example, if your IP address is 185.62.87.161 and the Flask server is running on port 5000, they would access it using http://185.62.87.161:5000/ in their web browsers.


## Deployment
1. After developing your application, you’ll want to make it available publicly to other users. You should use a dedicated WSGI server or hosting platform.

### Self-Hosted Options
1. Flask is a WSGI application. A WSGI server is used to run the application, converting incoming HTTP requests to the standard WSGI environ, and converting outgoing WSGI responses to HTTP responses.

2. We should run our WSGI application using a production WSGI server and HTTP server. There are many WSGI servers and HTTP servers, with many configuration possibilities. Detailed information regarding the platforms that can maange this for us can be found in the official Flask documentation: https://flask.palletsprojects.com/en/2.3.x/deploying/

3. WSGI servers have HTTP servers built-in. However, a dedicated HTTP server may be safer, more efficient, or more capable. Putting an HTTP server in front of the WSGI server is called a “reverse proxy.” Detailed information regarding how to do can be found in the official Flask documentation:
https://flask.palletsprojects.com/en/2.3.x/deploying/

### Hosting Platforms

1. There are many services available for hosting web applications without needing to maintain your own server, networking, domain, etc. Some services may have a free tier up to a certain time or bandwidth. Many of these services use one of the WSGI servers described above, or a similar interface

2. It is recommended to use **Microsoft Azure** to deploy the Python web app. Detailed information regarding how to do can be found in the official Flask documentation:
https://flask.palletsprojects.com/en/2.3.x/deploying/


_**Note:** The following link is a good tutorial to deploy Flask with a Linux server Gunicorn and Nginx :
https://dev.to/brandonwallace/deploy-flask-the-easy-way-with-gunicorn-and-nginx-jgc_


## Functionalities

1. Search and Select the channels that you want to visualize from the **'SELECT CHANNEL'** dropdown menus. You can select up to 5 channels.

2. Select the date/dates for which you want to visualize the data from the **'SELECT DATA'** dropdown menu. 

3. Select the frequency from the **'SELECT FREQUENCY:F'** text box at which you want to sample the data points. The default value is 60, which means one data point is sampled every 6 seconds. This is because the original data is sampled at every 0.1 seconds. Thus, the smallest frequency you can select is 1. However, it is important to note that the GUI will be slower as you decrease the frequency i.e. increase the sampling rate. 

4. Selecting these options will render the graphs for the selected channels as well as display the statistical data for those channels.

5. Select the specific time frame from the **'START TIME'** dropdown and **'END TIME'** dropdown menus and then click om the **'Update Graphs'** button. Doing so, will update all your graphs on the GUI for the selecetd time frame as well as display the statistics for that particular time frame. Then click on **'Reset Time'** button to reset the graphs to the original graphs.

6. You can hover on, zoom and pan the graphs. Then select the **'Reset Zoom'** button to reset the axes. 


## Additional codes for preliminary data analysis

1. This repo also contains two additional codes called `parquet.py` and `missingvalues.py` . Here we briefly discuss them:

### parquet.py:

1. This code is used to transform the available .parquet files in our static folder to a dataframe and perform basic data analysis for the required channels in order to identify outliers using the IQR method. 

2. Firstly, the function `parquet_to_dataframe_with_column_and_time` displays the values for the selected column of the selected file for the specific timeframe. This can be used as a sanity check to see if these values match those in the relevant .parquet file.

3. We can pre process the dataframe by removing rows with missing values and infinite values. We also find the channels with no variance and remove those channels from the dataframe. 

4. We then create a correlation heatmap for the selected file which is saved as an interactive .html file in:
`static/data/data_heatmaps` .

5. As a first step to detect outliers, we first would like to use if the channels that we are interested in follow a Gaussian distribution. While it is a good idea to do both visual and statistical tests, we go ahead with the visual test of plotting a histogram for our concerned channel. The histograms are saved in `static/data/data_anomalies` . 

6. It is seen that most of the channels don't follow a Gaussian distribution and that the data points are highly skewed.. This can be attributed to the way the data was logged, failures in the sensors etc.

7. We then employ the IQR(inter-quartile range) method to find the outliers for the selected channel. The following figure gives a comprehensive understanding about how to read a boxplot that uses IQR to detect outliers:
![IQR to detect Outliners](https://editor.analyticsvidhya.com/uploads/12311IQR.png)
The data points that lie 1.5 times of IQR above Q3 and below Q1 are outliers.

**Steps:**

- Sort the dataset in ascending order.
- Calculate the 1st and 3rd quartiles (Q1, Q3).
- Compute IQR = Q3 - Q1.
- Compute lower bound = (Q1 - 1.5 * IQR), upper bound = (Q3 + 1.5 * IQR).
- Loop through the values of the dataset and check for those that fall below the lower bound and above the upper bound. Mark them as outliers.

The resulting box plots would be saved as .png files in `static/data/data_anomalies/box_plots` .

8. These distribution and box plots give us an insight into the data. It's not difficult to understand that there are indeed many channels with skewed data. It is important to study these outliers for a particular channel independently as well in conjunction with other related channels.

9. To run the code pass the start time, end time, file name, column_names. For example:

 ```
$ (FH) python parquet.py --start-time 12:15:00 --end-time 12:20:50 --file-name 2023-05-31_OV71-JHX.parquet --column-names FCCU_PwrFuCellSysRaw Speed_kmh
```

### missingvalues.py:

1. This script helps us to determine the number of rows with missing values from each available .parquet file and the respective channels from which values are missing. The results are generated in missing_values.csv.

2. This script also helps us to determine the channels with values with no variance. The results are generated in zero_variance_features.csv.

3. Run the code by simply using:
   ```
   $ (FH) python missingvalues.py
   ```
