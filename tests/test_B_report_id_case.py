import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database
from app import app


class ReportIdCaseTest(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        db_path = str(Path(temp_dir.name) / "campusfix.db")
        database.init_db(db_path)

        db_patch = patch.object(database, "DB_PATH", db_path)
        db_patch.start()
        self.addCleanup(db_patch.stop)

        config_patch = patch.dict(
            app.config,
            {"TESTING": True, "SECRET_KEY": "test-only-key"},
        )
        config_patch.start()
        self.addCleanup(config_patch.stop)

        self.client = app.test_client()
        report = database.create_report(
            "Broken lamp",
            "Library",
            "Other",
            "The lamp is out.",
        )
        self.report_id = report["report_id"]

    def test_lowercase_id_returns_the_same_report(self):
        # The first report in the temporary database should be CF-1001.
        self.assertEqual(self.report_id, "CF-1001")

        uppercase = self.client.get("/api/reports/CF-1001")
        lowercase = self.client.get("/api/reports/cf-1001")

        self.assertEqual(uppercase.status_code, 200)
        self.assertEqual(lowercase.status_code, 200)

        uppercase_report = uppercase.get_json()["report"]
        lowercase_report = lowercase.get_json()["report"]

        self.assertEqual(uppercase_report["report_id"], "CF-1001")
        self.assertEqual(lowercase_report, uppercase_report)

    def test_staff_can_update_status_using_lowercase_id(self):
        with self.client.session_transaction() as session:
            session["role"] = "staff"

        response = self.client.post(
            f"/api/reports/{self.report_id.lower()}/status",
            json={"status": "In Progress"},
        )

        self.assertEqual(response.status_code, 200)
        report = database.get_report_by_id(self.report_id)
        self.assertEqual(report["status"], "In Progress")