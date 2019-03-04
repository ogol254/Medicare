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


class TestRecords(BaseTest):
    """This class collects all the test cases for the users"""

    def test_adding_records_admin(self):
        """Test that an admin user can add new record using a POST request"""
        record = self.post_records()
        self.assertEqual(record.status_code, 201)
        self.assertEqual(record.json['message'], "Success")

    def test_getting_records_admin(self):
        """Test that an admin user get all records using a GET request"""
        post = self.post_records()
        login = self.admin_login()
        token = login.json['AuthToken']
        get = self.get(path="/api/v1/records", auth=token)
        self.assertEqual(get.status_code, 200)
        self.assertEqual(get.json['message'], "records")

    def test_getting_single_record_admin(self):
        """Test that an admin user get all records using a GET request"""
        post = self.post_records()
        record_id = post.json['record_id']
        path = "/api/v1/records/{}".format(record_id)
        login = self.admin_login()
        token = login.json['AuthToken']
        get = self.get(path=path, auth=token)
        self.assertEqual(get.status_code, 200)
        self.assertEqual(get.json['message'], "record")
        self.assertTrue(get.json['records'])
        self.assertTrue(get.json['comments'])

    def test_editing_record_admin(self):
        """Test that an admin user get all records using a PUT request"""
        post = self.post_records()
        record_id = post.json['record_id']
        path = "/api/v1/records/{}".format(record_id)
        login = self.admin_login()
        token = login.json['AuthToken']
        data = {"status": "In-progres"}
        put = self.put(path=path, data=data, auth=token)
        self.assertEqual(put.status_code, 200)

    def test_unauthorized_records(self):
        """Test Unauthorised user requests in records"""
        """ For Getting """
        token = self.normal_login().json['AuthToken']
        get = self.get(path="/api/v1/records", auth=token)
        self.assertEqual(get.status_code, 401)

    def test_bad_request_records(self):
        """Test Bad user requests in incdents """
        get = self.get(path="/api/v1/records", auth=None)
        self.assertEqual(get.status_code, 400)

        """ Post """
        record = {
            "incident_id": self.post_incident().json['incident_id'],
            "id_num": self.user_admin['id_number'],
            "description": "3 months pregnant",
            "location": "Huruma",
            "facility_id": self.post_facilities().json['facility_id']
        }
        token = self.admin_login().json['AuthToken']
        res = self.post(path="/api/v1/records", data=record, auth=token)
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
