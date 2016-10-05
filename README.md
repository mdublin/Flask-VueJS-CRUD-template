[![Build Status](https://travis-ci.org/mdublin/Flask-VueJS-CRUD-template.svg?branch=master)](https://travis-ci.org/mdublin/Flask-VueJS-CRUD-template)

A simple CRUD Flask application that employs some Vue.js (includes delimiter alterations to not cause delimiter collisions with Jinja2).

**Setup**:

Step 1. Install virtualenv with `$ virtualenv env`

Step 2. Install dependencies with `$ pip install -r requirements/requirements.txt`

Step 3. Create postgres databases with `$ createdb CRUD` and `$ createdb CRUD-test`

Step 4. Create csrf token using:
        `>>> import os`
        `>>> os.urandom(24)`

        and set using environment variable `$ export CRUD_SECRET_KEY='{generated token}'`

To run:

`$ python manage.py runserver`

**Test**:

`$ python manage.py test --coverage`

Populate db with fake data:

`$ python manage.py seed`



