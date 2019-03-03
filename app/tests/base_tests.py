"""
This module tests the authentication endpoint
Authored by: ogol
"""
import unittest
import json
import string
from contextlib import closing
from random import choice, randint

# local imports
from .. import create_app
from ..db_config import destroy_db, init_db


class BaseTest(unittest.TestCase):
    """docstring for BaseTest"""
    api_prefix = "/api/v1/"

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user_admin = {
            "id_number": 33133243,
            "first_name": "Abraham",
            "last_name": "Ogol",
            "address": "Nairobi",
            "tell": "0790463533",
            "role": "admin",
            "password": "ogolpass"
        }

        self.user_clinician = {
            "id_number": 33133243,
            "first_name": "Abraham",
            "last_name": "Ogol",
            "address": "Nairobi",
            "tell": "0790463533",
            "role": "clinician",
            "password": "ogolpass"
        }

        self.user_normal = {
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
            self.db = init_db()

    def endpoint_path(self, path):
        return "/api/v1" + path

    def post(self, path, data, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=path, data=dto, headers=headers, content_type='application/json')
        return res

    def get(self, path, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=path, headers=headers, content_type='application/json')
        return res

    def put(self, path, data, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=path, data=dto, headers=headers, content_type='application/json')
        return res

    def delete(self, path, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=path, headers=headers, content_type='application/json')
        return res

    def post_user(self, role=""):
        if role == "Admin":
            res = self.post(path="/api/v1/users/32361391", data=self.user_admin, auth=None)
            return res
        elif role == "Normal":
            res = self.post(path="/api/v1/users/32361391", data=self.user_normal, auth=None)
            return res
        if role == "clinician":
            res = self.post(path="/api/v1/users/32361391", data=self.user_clinician, auth=None)
            return res

    def admin_login(self):
        register = self.post_user(role="Admin")
        login = self.post(path="/api/v1/auth/signin", data=self.user_admin, auth=None)
        return login

    def normal_login(self):
        register = self.post_user(role="Normal")
        login = self.post(path="/api/v1/auth/signin", data=self.user_normal, auth=None)
        return login

    def clinician_login(self):
        register = self.post_user(role="clinician")
        login = self.post(path="/api/v1/auth/signin", data=self.user_clinician, auth=None)
        return login

    def get_headers(self, authtoken=None):
        headers = {
            "Authorization": "Bearer {}".format(authtoken),
            "content_type": 'application/json'
        }
        return headers
