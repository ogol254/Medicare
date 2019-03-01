"""
This module tests the authentication endpoint
Authored by: ogol
"""
import unittest
import json
import string
from random import choice, randint

# local imports
from .. import create_app
from ..db_config import destroy_db, init_test_db


class TestAuth(unittest.TestCase):
    """This class collects all the test cases for the users"""

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user = {
            "id_number": 33133243,
            "first_name": "Abraham",
            "last_name": "Ogol",
            "address": "Nairobi",
            "tell": "0790463533",
            "role": "Normal",
            "password": "ogolpass"
        }

        self.error_msg = "The path accessed / resource requested cannot be found, please check"

        with self.app.app_context():
            self.db = init_test_db()

    def post_user(self, path='', data={}):
        if not data:
            data = self.user
        if not path:
            path = '/api/v1/users/32361391'
        # attempt to sign up
        res = self.client.post(path=path, data=json.dumps(data), content_type='application/json')
        return res

    def login(self, path="", data={}):
        register = self.post_user()
        if not data:
            data = self.user
        if not path:
            path = '/api/v1/auth/signin'
        # attempt to log in
        res = self.client.post(path=path, data=json.dumps(data), content_type='application/json')
        return res

    def test_user_signup(self):
        """Test that a user can signup using a POST request"""
        reg = self.post_user()
        self.assertEqual(reg.json['message'], 'Successfully added')
        self.assertEqual(reg.status_code, 201)

    def test_user_login(self):
        """Test that a user can login using a POST request"""
        data = {
            "id_number": self.user['id_number'],
            "password": self.user['password']
        }
        path = '/api/v1/auth/signin'
        login = self.login(path=path, data=data)
        self.assertEqual(login.json['message'], "Success")
        #self.assertEqual(login.status_code, 200)

    def test_user_logout(self):
        """Test that the user can logout using a POST request"""
        path = "/api/v1/auth/signout"
        login = self.login()
        token = login.json['AuthToken']
        headers = {"Authorization": "Bearer {}".format(token)}
        logout = self.client.post(path=path,
                                  headers=headers,
                                  content_type="application/json")
        self.assertEqual(logout.status_code, 200)

    def test_invalid_data(self):
        """Test that an unregistered user cannot log in"""
        # generate random username and password
        un_user = {
            "password": "".join(choice(
                                string.ascii_letters) for x in range(randint(7, 10))),
            "id_number": "".join(choice(
                string.ascii_letters) for x in range(randint(7, 10))),
        }
        # attempt to log in
        path = '/api/v1/auth/signin'
        login = self.login(path=path, data=un_user)
        self.assertEqual(login.status_code, 400)

    def test_an_unregistered_user(self):
        """Test that an unregistered user cannot log in"""
        data = {
            "id_number": 32781319,
            "password": "badadmnsn"
        }
        path = '/api/v1/auth/signin'
        login = self.login(path=path, data=data)
        self.assertEqual(login.status_code, 401)
        self.assertEqual(login.json['message'], "Your details were not found, please sign up")

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
