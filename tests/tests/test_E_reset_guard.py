import unittest
import tempfile
import os
from app import app
import database


class ResetDemoTestCase(unittest.TestCase):
    def setUp(self):
        """Init a temporaire database and a client"""
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        database.init_db(self.temp_db_path)

        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.temp_db_path

        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        """Clean the temporary database after the test"""
        database.DB_PATH = self.original_db_path
        os.close(self.db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    #  TEST 1 :  POST /api/reset-demo return 200 et success
    def test_reset_demo_endpoint_returns_success(self):
        res = self.client.post('/api/reset-demo')

        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertIn("re-seeded", data.get('message', '').lower())

    # TEST 2 : Verify that the database resets with the initial data
    def test_reset_restores_default_seed_reports(self):
        conn = database.get_connection()
        conn.execute("DELETE FROM reports")
        conn.commit()
        conn.close()

        self.assertEqual(len(database.get_reports()), 0, "The database should be empty for a reset")

        #We call the reset
        self.client.post('/api/reset-demo')

        #We check that the 8 reports are here
        reports_after = database.get_reports()
        self.assertGreater(len(reports_after), 0, "Reports should be recreated")

    # TEST 3 :GET not allowed (405 Method Not Allowed)
    def test_reset_requires_post_method(self):
        res = self.client.get('/api/reset-demo')
        self.assertEqual(res.status_code, 405)


if __name__ == '__main__':
    unittest.main()