import unittest
import tempfile
import os
from app import app
import database


class ResetDemoTestCase(unittest.TestCase):
    def setUp(self):
        """Initialize a temporary database and a temp client."""
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        database.init_db(self.temp_db_path)

        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.temp_db_path

        app.config['TESTING'] = True
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess['role'] = 'staff'

    def tearDown(self):
        """Clean up the temporary database after the test."""
        database.DB_PATH = self.original_db_path
        os.close(self.db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    #  TEST 1: /api/reset-demo return200 and success status
    def test_reset_demo_endpoint_returns_success(self):
        res = self.client.post('/api/reset-demo')

        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertIn("re-seeded", data.get('message', '').lower())

    # TEST 2: Verify reset repopulates initial seed reports
    def test_reset_restores_default_seed_reports(self):
        # Empty all reports from the temps database
        conn = database.get_connection()
        conn.execute("DELETE FROM reports")
        conn.commit()
        conn.close()

        self.assertEqual(len(database.get_reports()), 0, "Database should be empty before reset")

        # Trigger reset endpoint
        self.client.post('/api/reset-demo')

        # Verify seed reports are recreated
        reports_after = database.get_reports()
        self.assertGreater(len(reports_after), 0, "Reports should be recreated")

    #  TEST 3: Verify reset purges custom unseeded report
    def test_reset_cleans_custom_reports(self):
        # Add a temporary custom report
        database.create_report("Temp Issue", "Library", "Wi-Fi Failures", "Details")

        # Trigger reset
        self.client.post('/api/reset-demo')

        titles = [r['title'] for r in database.get_reports()]
        self.assertNotIn("Temp Issue", titles, "Custom reports must be removed after reset")

    # TEST 4: Verify idempotence across consecutive reset calls
    def test_reset_idempotency(self):
        # Multiple calls should not cause primary key conflicts
        for _ in range(3):
            res = self.client.post('/api/reset-demo')
            self.assertEqual(res.status_code, 200)

        self.assertEqual(len(database.get_reports()), 5, "Database must stay stable at 5 seed reports")

    #TEST 5: GET method rejected with 405 Method Not Allowed
    def test_reset_requires_post_method(self):
        res = self.client.get('/api/reset-demo')
        self.assertEqual(res.status_code, 405)

    # TEST 6: Student role rejected with 403 Forbidden
    def test_reset_denied_for_student(self):
        database.create_report("Student Issue", "Library", "Wi-Fi Failures", "Details")

        with self.client.session_transaction() as sess:
            sess['role'] = 'student'

        res = self.client.post('/api/reset-demo')
        self.assertEqual(res.status_code, 403)
        data = res.get_json()
        self.assertFalse(data.get('success'))

        titles = [r['title'] for r in database.get_reports()]
        self.assertIn("Student Issue", titles, "Custom reports must remain intact when reset is denied")


if __name__ == '__main__':
    unittest.main()
