import os
import unittest
from urlparse import urlparse
# Python 3 version:
#from urllib.parse import urlparse
from werkzeug.security import generate_password_hash

# THIS IS AN INTEGRATION TEST
# (tests that make sure the various subsystems, like the ORM and login system,
# are working correctly together)

# Using environent variable to configure app to use testing database, testing environment
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        # creating a test client using app.test_client function.
        # This allows us to make requests to views and inspect app responses
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user and add to db - user will be used to 
        # login and add test entry
        self.user = User(name="Alice", email="alice@example.com",
                        password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    # method to simulate logging in
    # this method mimics what Flask-login looks for to determine whether
    # a user is logged in or not. 
    def simulate_login(self):
        # this context manager uses self.client.session_transaction to get
        # access to a variable representing an HTTP session. 
        # two variables are added to this session: the id of the user and _fresh
        # which tells Flask-login that the session is still active. 
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    # method to simulate adding entry
    # in this method we call simulate_login to you can act as logged in user. 
    # Then you send a POST request to /entry/add using self.client.post
    # You use data parameter to provide form data for example entry.
    def test_add_entry(self):
        #calling this method so we can act as logged in user
        self.simulate_login()

        response = self.client.post("/entry/add", data={
            "title": "Test Entry",
            "content": "Test content"
        })
        print response
        # check that response from app looks ok
        self.assertEqual(response.status_code, 302)
        # make sure user is being redirected to / route by checking status code
        # and location header of the response.
        self.assertEqual(urlparse(response.location).path, "/")
        # check to make sure entry has been added to db correctly
        entries = session.query(Entry).all()
        # check to see that only one entry has been added 
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        # checking to see that title, content, and author are set to correct values
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user)


    def tearDown(self):
        """ Test teardown """
        print "Closing down..."
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

# to run this test:
# PYTHONPATH=. python tests/test_views_integration.py

if __name__ == "__main__":
    unittest.main()

