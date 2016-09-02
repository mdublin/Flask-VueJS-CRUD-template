from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# import the app Flask object from the blog package, courtesy of __init__.py
from blog import app

# engine object is created to as an object that talks to the db at the db URI specified in config.py

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base, engine
from sqlalchemy import Column, Integer, String, Text, DateTime

from .database import Base, engine

class Person(Base):
    __tablename__ = "Persons"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(500))
    lastname = Column(String(500))
    dob = Column(String(10))
    zipcode = Column(String(20))

Base.metadata.create_all(engine)

