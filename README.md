# GUI Visualization Tool

## Description

This basic GUI application is designed to provide a user-friendly interface for visualizing and analyzing user data. The data used for running this application are .parquet files. However, the code can be easily modified to read files of other types like .json or .csv. The GUI application was built on top of the Sneat - Bootstrap 5 HTML Admin Template - Pro | v1.0.0 (Product Page: [Sneat Bootstrap Admin Template](https://themeselection.com/products/sneat-bootstrap-html-admin-template/)) This repo is created to assist in a basic and high-level understanding of how to create a GUI application for different user needs. It is to be noted that the repo doesn't consist of any demo .parquet files, and originally it was developed for a time-series dataset, where one can visualize different data against time on the x-axis. Thus, you need to upload your own dataset (or any demo data) to the "static/data" directory.

**Development Stage:** In its current state, this GUI tool is actively under development. 
- **Backend:** The server-side code is written in Python using Flask.
- **Frontend:** The user interface is built with HTML and JavaScript.
 We are continuously working on improving its features, stability, and user experience.

## Functionalities

1. Search and Select the columns that you want to visualize from the **'SELECT CHANNEL'** dropdown menus. You can select up to 5 channels. (Here channel refers to the data/columns that you wish to visualize. You can change it according to the data you have)

2. From the **'SELECT DATA'** dropdown menu, select the date/dates for which you want to visualize the data. (This assumes you want to plot time-series data.)

3. Select the frequency from the **'SELECT FREQUENCY:F'** text box at which you want to sample the data points. The default value is 60, which means one data point is sampled every 6 seconds. This is because the original data that I used is sampled every 0.1 seconds. Thus, the smallest frequency you can select is 1. However, it is important to note that the GUI will be slower as you decrease the frequency i.e. increase the sampling rate. 

4. Selecting these options will render the graphs for the selected channels as well as display the statistical data for those channels.

5. Select the specific time frame from the **'START TIME'** dropdown and **'END TIME'** dropdown menus and then click om the **'Update Graphs'** button. Doing so will update all your graphs on the GUI for the selected time frame as well as display the statistics for that particular time frame. Then click on the **'Reset Time'** button to reset the graphs to the original graphs.

6. You can hover on, zoom and pan the graphs. Then select the **'Reset Zoom'** button to reset the axes.
7. You can modify the `graphindex.html` file (available in the "templates" folder) as per your needs and the structure and type of your data.

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
   git clone https://github.com/BhuyanMonami/GUI-Data-Visualization-Tool.git
   ```
### Step 3: Install Virtual Environment
1. Install `virtualenv`:
   ```
   $ pip install virtualenv
   ```
2. Open a terminal in the project root directory and run:
   ```
   $ virtualenv GUI
   ```
3. Then run the command:
   ```
   $ .\GUI\Scripts\activate
   ```
### Step 4: Install Flask and Dependencies 
1. Install Flask and SQLAlchemy:
   ```
   $ (GUI) pip install flask flask-sqlalchemy
   ```
   
## How to Run
1. Finally, start the web server:
   ```
   $ (GUI) python app.py
   ```

## Static files and Database

1. The code graphindex.html (in the "templates" folder) has a provision for fetching data from an SQLite database. 
2. Run the following code to add the .parquet files to the database after storing the files in the "static/data" directory:
   ```
   $ (GUI) python database.py
   ```

3. If you want to add more files to the database in future, you can do so by first storing them in the "static/data" directory.

This code will detect the new .parquet files in the "static/data" folder and insert them into the SQLite database as new tables while keeping the existing ones intact.

4. The database is currently saved as 'database.db' in the same directory where our Python script is located. In order to make it accessible to clients, the database (in our case, 'database.db') should be hosted on a server. This server can be a cloud-based server, a dedicated hosting server, or a server within your organization's network. The database server should be accessible to both your web application and the clients via a network connection.

## Further Optimization

The GUI platform needs to be tested under various conditions to find edge cases. It is to be noted that while it allows the user to choose the frequency at which data points are collected for rendering the graph, as one decreases the frequency, the platform becomes considerably slower. Further optimization of the code is needed in future development stages to address performance and memory issues.

## Access

1. Our Flask application will listen to all available network interfaces on your machine. In practical terms, it makes your application accessible from any device that can reach your machine over the network, including other devices on your local network and potentially over the internet (depending on your network and firewall settings).

2. You run `python app.py` on your machine, which starts the Flask development server and makes your web application accessible locally at http://localhost:5000/.

3. Other users on the same network can access your web application by using your machine's IP address and the port on which the Flask server is running. For example, if your IP address is 185.62.87.161 and the Flask server is running on port 5000, they would access it using http://185.62.87.161:5000/ in their web browsers.


## Deployment
1. After developing your application, you’ll want to make it available publicly to other users. You should use a dedicated WSGI server or hosting platform.

### Self-Hosted Options
1. Flask is a WSGI application. A WSGI server is used to run the application, converting incoming HTTP requests to the standard WSGI environ, and converting outgoing WSGI responses to HTTP responses.

2. We should run our WSGI application using a production WSGI server and HTTP server. There are many WSGI servers and HTTP servers with many configuration possibilities. Detailed information regarding the platforms that can manage this for us can be found in the official Flask documentation: https://flask.palletsprojects.com/en/2.3.x/deploying/

3. WSGI servers have HTTP servers built-in. However, a dedicated HTTP server may be safer, more efficient, or more capable. Putting an HTTP server in front of the WSGI server is called a “reverse proxy.” Detailed information regarding how to do so can be found in the official Flask documentation:
https://flask.palletsprojects.com/en/2.3.x/deploying/

### Hosting Platforms

1. There are many services available for hosting web applications without needing to maintain your own server, networking, domain, etc. Some services may have a free tier up to a certain time or bandwidth. Many of these services use one of the WSGI servers described above or a similar interface

2. It is recommended to use **Microsoft Azure** to deploy the Python web app. Detailed information regarding how to do so can be found in the official Flask documentation:
https://flask.palletsprojects.com/en/2.3.x/deploying/


_**Note:** The following link is a good tutorial to deploy Flask with a Linux server Gunicorn and Nginx :
https://dev.to/brandonwallace/deploy-flask-the-easy-way-with-gunicorn-and-nginx-jgc_
 
