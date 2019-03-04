"""
This module tests the authentication endpoint
Authored by: ogol
"""
import json
import string
import unittest
from contextlib import closing
from random import choice, randint

# local imports
from .. import create_app
from ..db_config import destroy_db, init_db

from .base_tests import BaseTest


class TestUserBio(BaseTest):
    """This class collects all the test cases for the users"""
    data = {"date_of_birth": "13/10/1995"}

    def test_posting_userbio(self):
        """Test that a user can add user bio using a POST request"""
        login = self.normal_login()
        token = login.json['AuthToken']
        path = "/api/v1/users/{}/bio".format(login.json['id_number'])
        post = self.post(path=path, data=self.data, auth=token)
        self.assertEqual(post.json['message'], 'Successfully added')
        self.assertEqual(post.status_code, 201)

    def test_getting_user_bio(self):
        """Test that a user can get bio using a GET request"""
        login = self.normal_login()
        token = login.json['AuthToken']
        path = "/api/v1/users/{}/bio".format(login.json['id_number'])
        post = self.post(path=path, data=self.data, auth=token)
        get = self.get(path=path, auth=token)
        self.assertEqual(get.status_code, 200)

    def test_editing_user_bio(self):
        login = self.normal_login()
        token = login.json['AuthToken']
        path = "/api/v1/users/{}/bio".format(login.json['id_number'])
        post = self.post(path=path, data=self.data, auth=token)
        data = {"blood_group": "B+"}
        put = self.put(path=path, data=self.data, auth=token)
        self.assertEqual(put.status_code, 200)

    def tearDown(self):
        """This function destroys objests created during the test run"""
        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
