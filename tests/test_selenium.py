import re
import threading
import time
import unittest
from selenium import webdriver
from CRUD import create_app, db
from CRUD.database import Person


class SeleniumTestCase(unittest.TestCase):
    '''
    the Flask server must be running in 'testing' mode for this to work.
    Make sure that you export FLASK_CONFIG='testing' before running this test
    as the shutdown route will only kill the server when the server is running
    in testing mode.
    '''
    
    client = None
    
    @classmethod
    def setUpClass(cls):
        # start Firefox
        try:
            #cls.client = webdriver.Firefox()
            cls.client = webdriver.Chrome()
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # create the database and populate with some fake data
            db.create_all()
            Person.seed
            #Role.insert_roles()
            #User.generate_fake(10)
            #Post.generate_fake(10)

            # add an administrator user
            #admin_role = Role.query.filter_by(permissions=0xff).first()
            #admin = User(email='john@example.com',
            #             username='john', password='cat',
            #             role=admin_role, confirmed=True)
            #db.session.add(admin)
            #db.session.commit()

            # start the Flask server in a thread
            threading.Thread(target=cls.app.run).start()
            # give the server a second to ensure it is up
            time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            print("INSIDE tearDownClass!!!")
            # stop the flask server and the browser
            cls.client.get('http://localhost:8080/shutdown')
            cls.client.close()
            #cls.client.quit()
            
            #time.sleep(2)

            # destroy database
            db.drop_all()
            db.session.remove()
            
            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_index(self):
        print("TEST INDEX IN SELENIUN CALLED!!!")
        # navigate to home page
        #self.client.get('http://localhost:8080/')
        self.client.get('http://localhost:8080/')
        time.sleep(2)
        self.assertTrue(re.search('CRUD \s+Demo', self.client.page_source))
        #self.assertTrue('<title>CRUD demo</title>' in self.client.page_source)

        # navigate to login page
        #self.client.find_element_by_link_text('Add Person').click()
        #self.assertTrue('<title>CRUD demo</title>' in self.client.page_source)

        # login
        #self.client.find_element_by_name('email').\
        #    send_keys('john@example.com')
        #self.client.find_element_by_name('password').send_keys('cat')
        #self.client.find_element_by_name('submit').click()
        #self.assertTrue(re.search('Hello,\s+john!', self.client.page_source))

        # navigate to the user's profile page
        #self.client.find_element_by_link_text('Profile').click()
        #self.assertTrue('<h1>john</h1>' in self.client.page_source)

