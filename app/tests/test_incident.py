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


class TestIncidents(BaseTest):
    """This class collects all the test cases for the users"""

    def test_adding_incidents_admin(self):
        """Test that an admin user can add new incident using a POST request"""
        incident = self.post_incident()
        self.assertEqual(incident.status_code, 201)
        self.assertEqual(incident.json['message'], "Success")

    def test_getting_incidents_admin(self):
        """Test that an admin user get all incidents using a GET request"""
        post = self.post_incident()
        login = self.admin_login()
        token = login.json['AuthToken']
        get = self.get(path="/api/v1/incidents", auth=token)
        self.assertEqual(get.status_code, 200)

    def test_getting_single_incident_admin(self):
        """Test that an admin user get all incidents using a GET request"""
        post = self.post_incident()
        incident_id = post.json['incident_id']
        path = "/api/v1/incidents/{}".format(incident_id)
        login = self.admin_login()
        token = login.json['AuthToken']
        get = self.get(path=path, auth=token)
        self.assertEqual(get.status_code, 200)

    def test_editing_incident_admin(self):
        """Test that an admin user get all incidents using a PUT request"""
        post = self.post_incident()
        incident_id = post.json['incident_id']
        path = "/api/v1/incidents/{}".format(incident_id)
        login = self.admin_login()
        token = login.json['AuthToken']
        data = {"status": "Verified"}
        put = self.put(path=path, data=data, auth=token)
        self.assertEqual(put.status_code, 200)

    def test_unauthorized_incidents(self):
        """Test Unauthorised user requests in incidents"""
        login = self.normal_login()
        token = login.json['AuthToken']

        """ For Getting """
        get = self.get(path="/api/v1/incidents", auth=token)
        self.assertEqual(get.status_code, 401)

    def test_bad_request_incidents(self):
        """Test Bad user requests in incdents """
        get = self.get(path="/api/v1/incidents", auth=None)
        self.assertEqual(get.status_code, 400)

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
