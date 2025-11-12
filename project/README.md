# Install and Setup
First things first you need to create a vitrual environment, this is done by:
`python3 -m vnev [name_of_venv]`
After doing this run:
`source venv/bin/activate`
This command will start up your virtual environment, next run
`pip install -r requirements`
This will then install all the neccesary packages for our project. When you
make changes to our depedencies or install new packages, please run:
`pip freeze > requirements.txt`
This will update the requirements list, with your new packages, `git push` this as 
soon as possible so everyone else can develop with them as well.

# Starting a Flask app
once you've finished setting up, you can now run it, this is done with:
`flask --app webapp run`
make sure you are in our projects root directory when running this. Upon
your first run, it should create a folder called instance/ this is where our
database is. 

