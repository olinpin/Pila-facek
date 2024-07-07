# Pila facek project

## How to run
1. Create a virtual environment for your project and install requirements with `pip install -r requirements.txt`
2. Clone the project
3. Setup the database and add environment variables to your .env file (as shown in database connection in `PilaFacek/settings.py`)
4. (Optional) Populate your database by running `python manage.py loaddata fixtures/data.json`
5. Run the project with `python manage.py runserver`


## How to deploy
1. Install the [elastic beanstalk CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html#eb-cli3-install.scripts)
2. Run `eb init` and login to aws
3. Commit and push your code
4. Run `eb deploy` to deploy