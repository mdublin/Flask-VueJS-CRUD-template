import os


#use this class to contain the configuration variables which control the Flask app. You set the location of your database, and tell Flask to use its debug mode to help you track down any errors in your application.


# This class is called in the __init__.py file in the config_path object
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://mdublin1@localhost:5432/CRUD"
    DEBUG = True
    # setting up secret key for Flask-login module
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")
    print SECRET_KEY


# creating separate db URI for testing and using different secret key
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://mdublin1@localhost:5432/CRUD-test"
    DEBUG = False
    SECRET_KEY = "Not secret"

# adding configuration to connect to Travis' Postgres db
class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/CRUD"
    DEBUG = False
    SECRET_KEY = "Not secret"

