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


class TestComments(BaseTest):
    """This class collects all the test cases for the comments"""

    def test_posting_comments(self):
        """Test that a user can add comment using a POST request"""
        post = self.post_comment()
        self.assertEqual(post.status_code, 201)

    def test_editing_comment(self):
        record = self.post_records()
        comment = self.post_comment()
        token = self.admin_login().json['AuthToken']
        path = "/api/v1/records/{}/comment/{}".format(record.json['record_id'], comment.json['comment_id'])
        data = {"comment": "Updated"}
        put = self.put(path=path, data=data, auth=token)
        self.assertEqual(put.status_code, 200)

    def tearDown(self):
        """This function destroys objests created during the test run"""
        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
