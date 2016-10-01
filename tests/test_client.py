import unittest, json
from CRUD import create_app, db
from CRUD.database import Person
from flask import url_for

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        #Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('CRUD Demo' in response.get_data(as_text=True))

    def test_addperson_page(self):
        response = self.client.get(url_for('main.addperson'))
        self.assertTrue('Review and submit' in response.get_data(as_text=True))

    def test_searchpeople_page(self):
        response = self.client.get(url_for('main.searchpeople'))
        self.assertTrue('Search by first name, last name, DOB, or postal code' in response.get_data(as_text=True))

    def test_addperson(self):
        response = self.client.post(url_for('main.addperson'), data=json.dumps(dict(firstname='Ozzy', lastname='Dinglehiemer', DOB='10/12/2000', postalCode='32108')), content_type='application/json')
        self.assertTrue(response.status_code == 200)
    
    def test_successconfirm(self):
        response = self.client.get(url_for('main.success_confirm'))
        self.assertTrue(response.status_code == 200)

    def test_deleteperson(self):
        response = self.client.post(url_for('main.searchpeople'), data=json.dumps(dict(delete_id='12')), content_type='application/json')
        self.assertTrue(response.status_code == 200)

    def test_updateperson(self):
        response = self.client.post(url_for('main.searchpeople'), data=json.dumps(dict(firstname='Pete', lastname='Bulger', DOB='12/12/1988', zipcode='12345', db_id='12', vue_page_index='12')), content_type='application/json')
        self.assertTrue(response.status_code == 200)


