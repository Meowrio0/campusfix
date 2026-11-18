"""
CampusFix - Part D: staff role switch requires a password.

Bug: any user could become staff with one click on "Switch Role".
Fix: POST /api/auth/switch with role='staff' must carry the password stored in
the CAMPUSFIX_STAFF_PASSWORD environment variable (never hard-coded in the repo).
"""

import os
import tempfile
import unittest
from unittest import mock

from app import app
import database

TEST_PASSWORD = 'unit-test-staff-password'


class StaffPasswordTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        database.init_db(self.temp_db_path)
        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.temp_db_path

        app.config['TESTING'] = True
        self.client = app.test_client()

        self.env_patch = mock.patch.dict(os.environ, {'CAMPUSFIX_STAFF_PASSWORD': TEST_PASSWORD})
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()
        database.DB_PATH = self.original_db_path
        os.close(self.db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def current_role(self):
        return self.client.get('/api/auth/current').get_json()['user']['role']

    def test_switch_to_staff_without_password_is_refused(self):
        res = self.client.post('/api/auth/switch', json={'role': 'staff'})
        self.assertEqual(res.status_code, 403)
        self.assertFalse(res.get_json()['success'])
        self.assertEqual(self.current_role(), 'student')

    def test_switch_to_staff_with_wrong_password_is_refused(self):
        res = self.client.post('/api/auth/switch', json={'role': 'staff', 'password': 'wrong'})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(self.current_role(), 'student')

    def test_switch_to_staff_with_non_string_password_is_refused(self):
        res = self.client.post('/api/auth/switch', json={'role': 'staff', 'password': 12345})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(self.current_role(), 'student')

    def test_switch_to_staff_with_correct_password_succeeds(self):
        res = self.client.post('/api/auth/switch', json={'role': 'staff', 'password': TEST_PASSWORD})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()['success'])
        self.assertEqual(res.get_json()['user']['role'], 'staff')
        self.assertEqual(self.current_role(), 'staff')

    def test_staff_access_disabled_when_password_not_configured(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            res = self.client.post('/api/auth/switch', json={'role': 'staff', 'password': ''})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(self.current_role(), 'student')

    def test_switch_back_to_student_needs_no_password(self):
        self.client.post('/api/auth/switch', json={'role': 'staff', 'password': TEST_PASSWORD})
        res = self.client.post('/api/auth/switch', json={'role': 'student'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.current_role(), 'student')

    def test_staff_obtained_with_password_can_update_status(self):
        """End-to-end: a refused switch keeps the student blocked; a valid one unlocks staff actions."""
        report = database.create_report(
            title='Broken projector', location='College of Law',
            category='Classroom Equipment', description='No image on screen.',
            db_path=self.temp_db_path
        )
        url = f"/api/reports/{report['report_id']}/status"
        update = {'status': 'Resolved', 'resolution_note': 'Replaced the projector lamp.'}

        self.client.post('/api/auth/switch', json={'role': 'staff', 'password': 'wrong'})
        self.assertEqual(self.client.post(url, json=update).status_code, 403)

        self.client.post('/api/auth/switch', json={'role': 'staff', 'password': TEST_PASSWORD})
        self.assertEqual(self.client.post(url, json=update).status_code, 200)


if __name__ == '__main__':
    unittest.main()
