#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, json
from flask.ext.script import Manager
# Instead of using argparse to pass commands to our blog app package, we are using a module called Flask-Script.
# Flask-Script allows you to specify tasks to help manage your application.

#from CRUD import app
from CRUD import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


manager = Manager(app)


#decorating run() with manager.command in order to add a command to a Flask-script Manager object
@manager.command
def run():
    port = int(os.environ.get('PORT', 8080)) #environ dictionary from os to get access to environment variables
    app.run(host='0.0.0.0', port=port)

# importing the database.py module from the blog package you created
#from CRUD.database import session, Person


@manager.command
def test():
    """ Run unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)





# populating the db with dummy content
@manager.command
def seed():
    '''
    populates CRUD db with dummy data crated here:
        http://www.generatedata.com/
    '''
    with open('dummy_data.json', 'r') as dummy_data:
        data = json.load(dummy_data)

    for index, item in enumerate(data):
        entry = Person(
            firstname = item["firstname"],
            lastname = item["lastname"],
            dob = item["dob"],
            zipcode = item["postalcode"]
        )
        session.add(entry)
    session.commit()


# this runs our seed() command:
# $ python manage.py seedi

#from flask.ext.migrate import Migrate, MigrateCommand
#from blog.database import Base

# create a new class for holding metadata object which Alembic uses to work out what changes to db schema need to happen.
#class DB(object):
#    def __init__(self, metadata):
#        self.metadata = metadata

# instantiating instance of Flask-Migrate's Migrate class, passing in app and an instance of the DB class.
#migrate = Migrate(app, DB(Base.metadata))
#adding all of the commands held in Migrate class to management script
#manager.add_command('db', MigrateCommand)


# to initialize the migration, run:

# $ python manage.py db init

# this command creates a folder called migrations
# that stoes the migration scripts and configuration for Alembic.


# Next, you need to create a migration script by running:

# $ python manage.py db migrate

# this will create a new file in migrations/versions folder that might be something like d05e1078c80_.py
# this contains two functions, one for upgrading the db and one for downgrading it.

# The upgrade function should contain a line which adds the foreign key to the entries table, and the downgrade function should remove the foreign key.

# Changes to the db have been automatically calcuated by Alembic.


# Run the migration script to actually apply the changes to the database:

# $ python manage.py db upgrade

# this runs the upgrade function, adding column to db table.


# In summation:
# each time you make a change to the db you need to run the following to generate a migration script:

# $ python manage.py db migrate

# to apply changes:

# $ python manage.py db upgrade

# if you need to roll back changes at any point, then the following will reverse a migration:

# $ python manage.py downgrade

# that's all there is to changing datbase schema. 

if __name__ == "__main__":
    manager.run()

