# Install and Setup
First things first you need to create a vitrual environment, this is done by:
```bash
# Creates a new virtual python environemnt
python3 -m vnev [name_of_venv]
# Activates this environment
source venv/bin/activate
# Installs all requirements from requirements.txt
pip install -r requirements.txt
```
This will then install all the neccesary packages for our project. 

# Starting a Flask app
once you've finished setting up, you can now run it, this is done with:
```bash
flask --app webapp run
```
make sure you are in our projects root directory when running this. Upon
your first run, it should create a folder called instance/ this is where our
database is. 

# Intializing the Database
After setting up the flask app, you should be able to run the following commands:
```bash
# This will ensure your database has all the correct tables
flask --app webapp init-db
# This will add all our seed data to your instance db
flask --app webapp seed-db
```

# Making changes
When you make changes to our depedencies or install new packages, please run:
```bash
pip freeze > requirements.txt
```
This will update the requirements list, with your new packages, `git push` this as 
soon as possible so everyone else can develop with them as well.
