# Install and Setup
There are two methods to download and run our project:

### 1. Using Build.py
On MacOS/Linux or Windows you can use our build script to do most of the setup process.
The build script will create a virtual environment, install all our depedencies, then initalize 
our database. To install:
```bash
# Ensure you are inside our source directory
python3 build.py
source venv/bin/activate  # on MacOS/Linux
venv\Scripts\activate.bat # on Windows (CMD)
# You're all set to run the project
flask --app webapp run
```

### 2. Not Using Build.py
First things first you need to create a vitrual environment, this is done by:
```bash
# Ensure you are inside our source directory
# Creates a new virtual python environemnt
python3 -m venv [name_of_venv] 
# Activates this environment
source venv/bin/activate  # for Mac/Linux
# or for Windows (CMD)
venv\Scripts\activate.bat
# Installs all requirements from requirements.txt
pip install -r requirements.txt
```
After setting up the flask app, you should be able to run the following commands in 
`source/`:
```bash
# This will build the sqlite database and load the seed data
flask --app webapp reset-db
```
This will then install all the neccesary packages for our project. 
Once you've finished setting up, you can now run it. Ensure you are in your
virtual environment installed previously, and you are in the `source/` dir. Then:
```bash
flask --app webapp run
```
# Database Commands
Our `db.py` files comes with some click commands that can be used for database operations
```bash
flask --app webapp init-db  # Sets up the SQLite data with the appropriate columns
flask --app webapp seed-db  # Loads seed data into the database, this will duplicate data if run more than once
flask --app webapp reset-db  # Deletes the current database instance, and rebuilds it with seed data
```
# Making Changes
When you make changes to our depedencies or install new packages, please run:
```bash
pip freeze > requirements.txt
```
This will update the requirements list, with your new packages, `git push` this as 
soon as possible so everyone else can develop with them as well.
