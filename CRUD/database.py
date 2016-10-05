from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# import the app Flask object from the blog package, courtesy of __init__.py
from . import db
# engine object is created to as an object that talks to the db at the db URI specified in config.py


#engine = create_engine(CRUD.config["SQLALCHEMY_DATABASE_URI"])
#Base = declarative_base()
#Session = sessionmaker(bind=engine)
#session = Session()

import datetime
#from sqlalchemy import Column, Integer, String, Text, DateTime
#from .database import Base, engine
import json

import os
#using abspath here for json file so that selenium_test.py can run Person.seed()
# or else you get IOError 2 file does not exist
dummy_file = os.path.abspath("CRUD/dummy_data.json")


class Person(db.Model):
    __tablename__ = "Persons"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(500))
    lastname = db.Column(db.String(500))
    dob = db.Column(db.String(10))
    zipcode = db.Column(db.String(20))

    # populate database with fake users
    @staticmethod
    def seed():
        """
        same method that's in manage.py
        """
        with open(dummy_file, 'r') as dummy_data:
            data = json.load(dummy_data)
        for index, item in enumerate(data):
            entry = Person(
                firstname = item["firstname"],
                lastname = item["lastname"],
                dob = item["dob"],
                zipcode = item["postalcode"]
            )
            db.session.add(entry)
        db.session.commit()
    
        
#Base.metadata.create_all(engine)


