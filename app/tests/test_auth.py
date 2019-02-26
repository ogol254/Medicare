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
            "password": "admin",
            "id_number": "123456789"
        }
        self.error_msg = "The path accessed / resource requested cannot be found, please check"

        with self.app.app_context():
            self.db = init_test_db()

    def login(self, path="/api/v1/auth/signin", data={}):

        if not data:
            data = self.user
        # attempt to log in
        res = self.client.post(path=path, data=json.dumps(data), content_type='application/json')
        return res

    def test_user_login(self):
        """Test that a user can login using a POST request"""
        login = self.login()
        #self.assertEqual(login.json['message'], 'Success')
        self.assertTrue(login.json['AuthToken'])
        #self.assertEqual(login.status_code, 401)

    # def test_user_logout(self):
    #     """Test that the user can logout using a POST request"""
    #     new_user = self.post_data().json
    #     path = "/api/v1/auth/logout"
    #     token = new_user['AuthToken']
    #     headers = {"Authorization": "Bearer {}".format(token)}
    #     logout = self.client.post(path=path,
    #                               headers=headers,
    #                               content_type="application/json")
    #     self.assertEqual(logout.status_code, 200)
    #     logout_again = self.client.post(path=path,
    #                                     headers=headers,
    #                                     content_type="application/json")
    #     self.assertEqual(logout_again.status_code, 401)

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
        login = self.client.post('/api/v1/auth/signin', data=json.dumps(un_user), content_type='application/json')
        self.assertEqual(login.status_code, 400)

    # def test_an_unregistered_user(self):
    #     """Test that an unregistered user cannot log in"""
    #     # generate random username and password
    #     un_user = {
    #         }
    #     # attempt to log in
    #     login = self.client.post('/api/v1/auth/signin', data=json.dumps(un_user), content_type='application/json')
    #     #self.assertEqual(login.status_code, 400)
    #     self.assertEqual(login.json['message'], "Not found")

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
