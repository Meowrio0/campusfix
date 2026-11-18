"""
Part A - Report title length limit.

Bug: a report with a 5000-character title was accepted.
Fix: titles longer than MAX_TITLE_LENGTH (100) are rejected with HTTP 400
and a field-specific error message.
"""

import os
import tempfile
import unittest

import database
from app import app, MAX_TITLE_LENGTH


class TitleLengthTestCase(unittest.TestCase):
    def setUp(self):
        """Use a fresh temporary database for each test."""
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        database.init_db(self.temp_db_path)
        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.temp_db_path
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        os.close(self.db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def make_payload(self, title):
        return {
            "title": title,
            "location": "Library",
            "category": "Wi-Fi Failures",
            "description": "Wi-Fi keeps disconnecting on the 3rd floor."
        }

    def test_A1_title_over_limit_is_rejected(self):
        """A title one character over the limit returns 400 with a title error."""
        res = self.client.post('/api/reports', json=self.make_payload("x" * (MAX_TITLE_LENGTH + 1)))
        self.assertEqual(res.status_code, 400)
        self.assertIn('title', res.get_json()['errors'])

    def test_A2_title_at_limit_is_accepted(self):
        """A title of exactly the limit is still accepted."""
        res = self.client.post('/api/reports', json=self.make_payload("x" * MAX_TITLE_LENGTH))
        self.assertEqual(res.status_code, 201)

    def test_A3_5000_character_title_is_rejected_and_not_saved(self):
        """The original bug: a 5000-character title must be rejected and nothing saved."""
        res = self.client.post('/api/reports', json=self.make_payload("x" * 5000))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.client.get('/api/reports').get_json()['count'], 0)


if __name__ == '__main__':
    unittest.main()
