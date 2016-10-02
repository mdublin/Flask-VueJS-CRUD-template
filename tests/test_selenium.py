import unittest
import re
import threading
from flask import current_app
from CRUD import create_app, db
from CRUD.database import Person
from selenium import webdriver

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
    # cls is defined in PEP8 as argument passed to class methods vs self for instance methods
    # start Firefox
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")
        
            # create the database and populate with some fake data
            db.create_all()
            Person.seed()

            # start the Flask server in a thread
            threading.Thread(target=cls.app.run).start()
    
    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the flask server and the browser
            cls.client.get('http://0.0.0.0:8080/shutdown')
            cls.client.close()

            # destroy database
            db.drop_all()
            db.session.remove()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('web browser not available')

    def tearDown(self):
        pass

    def test_index(self):
        self.client.get('http://0.0.0.0:8080/')
        self.assertTrue('<h1>CRUD Demo</h1>' in self.client.page_source)


