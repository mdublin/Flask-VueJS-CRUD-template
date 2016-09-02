import os
import unittest

# multiprocessing module provides the ability to start and run other code 
# simultaneously with other scripts --> it provides features for implementing
# concurrency in oder to use multiprocessing. It also allows you to communicate
# and control this code by calling methods start and terminate. 
import multiprocessing

import time

from urlparse import urlparse

from werkzeug.security import generate_password_hash

# spinter is Python layer for Selenium
from splinter import Browser

# Configure your app to user the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User


class TestViews(unittest.TestCase):

    def setUp(self):
        """ Test setup """

        # creating instance of splinter.Browser class, using PhantomJS driver
        self.browser = Browser("firefox")

        # Set up the tables in the db
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = User(name="Alice", email="alice@example.com",
                        password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        # Using the multiprocessing module in oder to start the Flask test server
        # because the test will be visiting the actual site you need a server up
        # to run the app.
        # we can not just call app.run method as usual because it will stop the 
        # tests from running after it has started. 
        # Instead we launch app.run in a spearate process via an instance of 
        # multiprocessing.Process
        # The target tells it which function to run, in this case your app.run
        # method, we then start the process by using its start method. However
        # we need to wait for a bit for the server to start, so we use
        # time.sleep(1) in order to pause code execution for a second. 
        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1)

    # how we kill the server
    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the db

        # kill server using process.terminate method
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        # exit browser using browser.quit method
        self.browser.quit()


    # tests using browser to check whether or not login works

    def test_login_correct(self):
        # visit login page using browser.visit method
        self.browser.visit("http://127.0.0.1:5000/login")
        # fill in form fields using browser.fill method
        # this looks for <input> element in html which has name attribute
        # matching the first argument, which in these case are email and
        # password fields, then fills in these with info given in second argument
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        # locate submit button using css selector rules to find item on page
        # in this case, we are looking for <button> element which has type 
        # attribute set to submit
        button = self.browser.find_by_css("button[type=submit]")
        # use click method to submit form
        button.click()
        # checking to see if we have been relocated to the front page after
        # successful login
        print self.browser.url
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
    
    
    def test_login_incorrect(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "fred@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")


if __name__ == "__main__":
    unittest.main()

