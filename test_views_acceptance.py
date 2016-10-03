import os
import unittest
import multiprocessing
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
#os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from CRUD import create_app, db
from CRUD.database import Person


class TestViews(unittest.TestCase):
    
    @classmethod
    def setUp(cls):
        """ Test setup """
        cls.browser = Browser("phantomjs")

        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()
        # Set up the tables in the database
        #Base.metadata.create_all(engine)

        # Create an example user
        #self.user = User(name="Alice", email="alice@example.com",
        #                 password=generate_password_hash("test"))
        #session.add(self.user)
        #session.commit()

        cls.process = multiprocessing.Process(target=cls.app.run, kwargs={"port": 8080})
        cls.process.start()
        time.sleep(2)

    @classmethod
    def tearDown(cls):
        """ Test teardown """
        # Remove the tables and their data from the database
        #cls.process.terminate()
        db.drop_all()
        cls.session.remove()
        #session.close()
        #engine.dispose()
        #Base.metadata.drop_all(engine)
        cls.browser.quit()
        cls.app_context.pop()




    def test_index(self):
        self.browser.visit("http://localhost:8080/")
        #self.browser.fill("email", "alice@example.com")
        #self.browser.fill("password", "test")
        #button = self.browser.find_by_css("button[type=submit]")
        #button.click()
        self.assertEqual(self.browser.url, "http://localhost:8080/")



'''
    def test_login_incorrect(self):
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/login")


if __name__ == "__main__":
    unittest.main()

'''