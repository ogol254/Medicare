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

from .base_tests import BaseTest


class TestFacilities(BaseTest):
    """This class collects all the test cases for the users"""

    def test_adding_facilities_admin(self):
        """Test that an admin user can add new facility using a POST request"""
        facility = self.post_facilities()
        self.assertEqual(facility.status_code, 201)
        self.assertEqual(facility.json['message'], "Success")
        self.assertTrue(facility.json['facility_id'])

    def test_getting_facilities_admin(self):
        """Test that an admin user get all facilities using a GET request"""
        post = self.post_facilities()
        login = self.admin_login()
        token = login.json['AuthToken']
        get = self.get(path="/api/v1/facilities", auth=token)
        self.assertEqual(get.status_code, 200)

    def test_getting_single_facility_admin(self):
        """Test that an admin user get all facilities using a GET request"""
        post = self.post_facilities()
        facility_id = post.json['facility_id']
        path = "/api/v1/facilities/{}".format(facility_id)
        login = self.admin_login()
        token = login.json['AuthToken']
        get = self.get(path=path, auth=token)
        self.assertEqual(get.status_code, 200)

    def test_editing_facility_admin(self):
        """Test that an admin user get all facilities using a PUT request"""
        post = self.post_facilities()
        facility_id = post.json['facility_id']
        path = "/api/v1/facilities/{}".format(facility_id)
        login = self.admin_login()
        token = login.json['AuthToken']
        data = {"name": "KNH"}
        put = self.put(path=path, data=data, auth=token)
        self.assertEqual(put.status_code, 200)

    def test_unauthorized(self):
        """Test Unauthorised user requests"""
        login = self.normal_login()
        token = login.json['AuthToken']

        """ For Posting """
        post = self.post(path="/api/v1/facilities", data=self.facility, auth=token)
        self.assertEqual(post.status_code, 401)

        """ For Getting """
        get = self.get(path="/api/v1/facilities", auth=token)
        self.assertEqual(get.status_code, 401)

    def test_bad_request(self):
        """Test Bad user requests"""
        get = self.get(path="/api/v1/facilities", auth=None)
        self.assertEqual(get.status_code, 400)

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
