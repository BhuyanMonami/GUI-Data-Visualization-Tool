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
### Step 1: Install Python 3.8 or Newer

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
sudo apt install python3.8
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

Currently, the static files are loaded in the static/data directory as .parquet files. Additional and new files can be added to the same directory. The repo shall be updated when the files are stored in a database. 
