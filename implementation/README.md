# Implementation

## Environment Setup
Make sure that you have Python 3.11 or greater installed. See [here](https://www.python.org/downloads/) if you do not already have it installed.

There are two methods to download and run our project:

### 1. Using Build.py
On MacOS/Linux or Windows you can use our build script to do most of the setup process.
The build script will create a virtual environment, install all our depedencies, then initalize 
our database. To install:
```bash
# Ensure you are inside our source directory
python3 build.py
source venv/bin/activate  # for MacOS/Linux
venv\Scripts\activate.bat # or for Windows (CMD)
```

### 2. Not Using Build.py
First things first you need to create a vitrual environment, this is done by:
```bash
# Ensure you are inside our source directory
python3 -m venv venv # Creates a new virtual python environemnt

# Activates this environment
source venv/bin/activate  # for MacOS/Linux
venv\Scripts\activate.bat # or for Windows (CMD)

# Installs all requirements from requirements.txt
pip install -r requirements.txt
```

## Database Setup
After setting up the flask app, you should be able to setup the database (still in `source/`):
```bash
# This will build the sqlite database and load the seed data
flask --app webapp reset-db
``` 

## How to Start and Login
Once you've finished setting up, you can now run it. Ensure you are in your
virtual environment installed previously, and you are in the `source/` dir. Then:
```bash
flask --app webapp run
```
Open the link that is provided on run.

You should be at the login page now. You can either register a new regular user or log-in as the seed admin using the following information:

```
Email:
ronsemail@example.com

Password:
admin1
```

## Troubleshooting
Our `db.py` files comes with some click commands that can be used for database operations
```bash
flask --app webapp init-db  # Sets up the SQLite data with the appropriate columns
flask --app webapp seed-db  # Loads seed data into the database, this will duplicate data if run more than once
flask --app webapp reset-db  # Deletes the current database instance, and rebuilds it with seed data
```
### Making Changes
When you make changes to our depedencies or install new packages, please run:
```bash
pip freeze > requirements.txt
```
This will update the requirements list, with your new packages, `git push` this as 
soon as possible so everyone else can develop with them as well.
