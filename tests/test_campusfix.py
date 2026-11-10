"""
CampusFix - Automated Test Suite
National Taipei University / Software Engineering
Team: SE_CampusFix_Team04

Covers all 10 required test cases specified in Section 10 of assignment:
1. Valid report submission (CF-10)
2. Missing required field (CF-11)
3. Unique IDs for separate reports (CF-12)
4. Persistence after refresh and restart (CF-13)
5. Correct report details and status (CF-14)
6. Keyword search, including different letter case (CF-21)
7. Location filtering (CF-22)
8. Search with no matches (CF-23)
9. Staff update and required resolution note (CF-31)
10. Student prevented from staff update actions (CF-32)
11. Combined filter logical AND behavior (CF-22)
"""

import unittest
import os
import tempfile
import json
from app import app
import database

class CampusFixTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a fresh temporary SQLite database and test client for each test."""
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        database.init_db(self.temp_db_path)
        
        # Point database module to our temp DB for testing
        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.temp_db_path
        
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        self.client = app.test_client()

    def tearDown(self):
        """Clean up temporary test database."""
        database.DB_PATH = self.original_db_path
        os.close(self.db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    # -------------------------------------------------------------
    # Test Case 1: Valid report submission (Story CF-10)
    # -------------------------------------------------------------
    def test_01_valid_report_submission(self):
        """Test ID: TC-01 - Valid report submission saves all fields and returns 201."""
        payload = {
            "title": "Broken HDMI cable in Room 301",
            "location": "College of Business",
            "category": "Classroom Equipment",
            "description": "HDMI cable at the lectern has bent pins and cannot connect to laptop."
        }
        res = self.client.post('/api/reports', json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('report', data)
        self.assertEqual(data['report']['title'], payload['title'])
        self.assertEqual(data['report']['location'], payload['location'])
        self.assertEqual(data['report']['category'], payload['category'])
        self.assertEqual(data['report']['description'], payload['description'])
        self.assertEqual(data['report']['status'], 'Submitted')
        self.assertTrue(data['report']['report_id'].startswith('CF-'))

    # -------------------------------------------------------------
    # Test Case 2: Missing required field (Story CF-11)
    # -------------------------------------------------------------
    def test_02_missing_required_field(self):
        """Test ID: TC-02 - Missing required fields prevent submission and return 400 with field errors."""
        payload = {
            "title": "   ",
            "location": "Library",
            "category": "Wi-Fi Failures",
            "description": ""
        }
        res = self.client.post('/api/reports', json=payload)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data['success'])
        self.assertIn('errors', data)
        self.assertIn('title', data['errors'])
        self.assertIn('description', data['errors'])

    # -------------------------------------------------------------
    # Test Case 3: Unique IDs for separate reports (Story CF-12)
    # -------------------------------------------------------------
    def test_03_unique_ids_for_separate_reports(self):
        """Test ID: TC-03 - Consecutively created reports receive distinct unique IDs."""
        p1 = {
            "title": "Broken window blind",
            "location": "Library",
            "category": "Damaged Facilities",
            "description": "Blinds on 2F cannot be pulled down."
        }
        p2 = {
            "title": "Restroom tap leaking",
            "location": "College of Law",
            "category": "Plumbing & Restroom",
            "description": "Sink tap dripping continuously."
        }
        r1 = self.client.post('/api/reports', json=p1).get_json()['report']
        r2 = self.client.post('/api/reports', json=p2).get_json()['report']
        
        self.assertNotEqual(r1['report_id'], r2['report_id'])
        self.assertNotEqual(r1['id'], r2['id'])

    # -------------------------------------------------------------
    # Test Case 4: Persistence after refresh and restart (Story CF-13)
    # -------------------------------------------------------------
    def test_04_persistence_after_restart(self):
        """Test ID: TC-04 - Data survives application/client reconnection from disk."""
        payload = {
            "title": "Persistent projector issue",
            "location": "College of Social Sciences",
            "category": "Classroom Equipment",
            "description": "Projector fan makes loud buzzing noise."
        }
        post_res = self.client.post('/api/reports', json=payload).get_json()
        report_id = post_res['report']['report_id']

        fresh_report = database.get_report_by_id(report_id, db_path=self.temp_db_path)
        self.assertIsNotNone(fresh_report)
        self.assertEqual(fresh_report['title'], payload['title'])
        self.assertEqual(fresh_report['status'], 'Submitted')

    # -------------------------------------------------------------
    # Test Case 5: Correct report details and status (Story CF-14)
    # -------------------------------------------------------------
    def test_05_correct_report_details_and_status(self):
        """Test ID: TC-05 - GET endpoint returns exact details, timestamps, and status."""
        created = database.create_report(
            title="Mic volume too low",
            location="Sports Center & Gymnasium",
            category="Classroom Equipment",
            description="Wireless mic battery is dead.",
            db_path=self.temp_db_path
        )
        res = self.client.get(f"/api/reports/{created['report_id']}")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()['report']
        self.assertEqual(data['title'], "Mic volume too low")
        self.assertEqual(data['status'], "Submitted")
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    # -------------------------------------------------------------
    # Test Case 6: Keyword search, including different letter case (Story CF-21)
    # -------------------------------------------------------------
    def test_06_keyword_search_case_insensitive(self):
        """Test ID: TC-06 - Keyword search in title/description is case-insensitive."""
        database.create_report(
            title="Eduroam Wi-Fi Disconnection",
            location="Library",
            category="Wi-Fi Failures",
            description="Laptops lose connection on the 4th floor.",
            db_path=self.temp_db_path
        )
        database.create_report(
            title="Broken Chair Armrest",
            location="College of Business",
            category="Damaged Facilities",
            description="Plastic armrest snapped in lecture hall.",
            db_path=self.temp_db_path
        )

        res_lower = self.client.get('/api/reports?keyword=wi-fi').get_json()
        self.assertEqual(res_lower['count'], 1)
        self.assertEqual(res_lower['reports'][0]['title'], "Eduroam Wi-Fi Disconnection")

        res_upper = self.client.get('/api/reports?keyword=WI-FI').get_json()
        self.assertEqual(res_upper['count'], 1)

        res_desc = self.client.get('/api/reports?keyword=4TH%20FLOOR').get_json()
        self.assertEqual(res_desc['count'], 1)

    # -------------------------------------------------------------
    # Test Case 7: Location filtering (Story CF-22)
    # -------------------------------------------------------------
    def test_07_location_filtering(self):
        """Test ID: TC-07 - Filtering by campus location returns only reports for that location."""
        database.create_report(
            title="Water dispenser filter red light",
            location="Library",
            category="Plumbing & Restroom",
            description="Filter needs replacement.",
            db_path=self.temp_db_path
        )
        database.create_report(
            title="Broken desk lock",
            location="College of Business",
            category="Damaged Facilities",
            description="Lock is jammed.",
            db_path=self.temp_db_path
        )

        res = self.client.get('/api/reports?location=Library').get_json()
        self.assertEqual(res['count'], 1)
        self.assertEqual(res['reports'][0]['location'], "Library")

    # -------------------------------------------------------------
    # Test Case 8: Search with no matches (Story CF-23)
    # -------------------------------------------------------------
    def test_08_search_with_no_matches(self):
        """Test ID: TC-08 - Search query with no matching keywords returns empty list cleanly."""
        database.create_report(
            title="Light fixture humming",
            location="Library",
            category="Damaged Facilities",
            description="Fluorescent tube hums loudly.",
            db_path=self.temp_db_path
        )
        res = self.client.get('/api/reports?keyword=nonexistent_xyz_query').get_json()
        self.assertEqual(res['count'], 0)
        self.assertEqual(len(res['reports']), 0)

    # -------------------------------------------------------------
    # Test Case 9: Staff update and required resolution note (Story CF-31)
    # -------------------------------------------------------------
    def test_09_staff_update_and_required_resolution_note(self):
        """Test ID: TC-09 - Staff can update status; marking Resolved requires non-empty resolution note."""
        rep = database.create_report(
            title="Air conditioning failure",
            location="College of Law",
            category="Classroom Equipment",
            description="AC unit not cooling in Room L101.",
            db_path=self.temp_db_path
        )
        
        with self.client.session_transaction() as sess:
            sess['role'] = 'staff'
            sess['email'] = 'staff@ntpu.edu.tw'

        fail_res = self.client.post(f"/api/reports/{rep['report_id']}/status", json={
            "status": "Resolved",
            "resolution_note": "    "
        })
        self.assertEqual(fail_res.status_code, 400)
        self.assertIn("resolution note is required", fail_res.get_json()['error'])

        success_res = self.client.post(f"/api/reports/{rep['report_id']}/status", json={
            "status": "Resolved",
            "resolution_note": "Replaced thermostat sensor and recharged refrigerant. Verified 23C."
        })
        self.assertEqual(success_res.status_code, 200)
        updated = success_res.get_json()['report']
        self.assertEqual(updated['status'], 'Resolved')
        self.assertIn("Replaced thermostat", updated['resolution_note'])

    # -------------------------------------------------------------
    # Test Case 10: Student prevented from staff update actions (Story CF-32)
    # -------------------------------------------------------------
    def test_10_student_prevented_from_staff_update_actions(self):
        """Test ID: TC-10 - Student role is rejected with 403 Forbidden when attempting status changes."""
        rep = database.create_report(
            title="Elevator door button jammed",
            location="College of Electrical Engineering & Computer Science",
            category="Damaged Facilities",
            description="Open door button gets stuck in depressed position.",
            db_path=self.temp_db_path
        )

        with self.client.session_transaction() as sess:
            sess['role'] = 'student'
            sess['email'] = 'student@ntpu.edu.tw'

        res = self.client.post(f"/api/reports/{rep['report_id']}/status", json={
            "status": "In Progress"
        })
        self.assertEqual(res.status_code, 403)
        data = res.get_json()
        self.assertFalse(data['success'])
        self.assertIn("Access denied", data['error'])

    # -------------------------------------------------------------
    # Additional Test: Combined filters AND logic behavior
    # -------------------------------------------------------------
    def test_11_combined_filters_and_logic(self):
        """Test ID: TC-11 - Combined keyword and location filters behave as AND logic."""
        database.create_report(
            title="Projector broken",
            location="Library",
            category="Classroom Equipment",
            description="Bulb dead in reading room.",
            db_path=self.temp_db_path
        )
        database.create_report(
            title="Projector broken",
            location="College of Business",
            category="Classroom Equipment",
            description="Remote control missing.",
            db_path=self.temp_db_path
        )

        res = self.client.get('/api/reports?keyword=Projector&location=Library').get_json()
        self.assertEqual(res['count'], 1)
        self.assertEqual(res['reports'][0]['location'], "Library")

if __name__ == '__main__':
    unittest.main()
