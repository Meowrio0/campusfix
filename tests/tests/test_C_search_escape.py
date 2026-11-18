
import unittest
import os
import tempfile
import database


class TestCSearchEscape(unittest.TestCase):

    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        database.init_db(self.db_path)

        for title in [
            "Battery at 100% capacity",
            "Battery at 100X capacity",
            "Room A_B projector broken",
            "Room A1B projector broken",
            r"Path C:\temp unavailable",
        ]:
            database.create_report(
                title=title,
                location="Library",
                category="Equipment",
                description="Test report",
                db_path=self.db_path,
            )

    def tearDown(self):
        os.remove(self.db_path)

    def test_percent_literal(self):
        results = database.get_reports(
            keyword="100%", db_path=self.db_path
        )
        self.assertEqual(
            [r["title"] for r in results],
            ["Battery at 100% capacity"],
        )

    def test_underscore_literal(self):
        results = database.get_reports(
            keyword="A_B", db_path=self.db_path
        )
        self.assertEqual(
            [r["title"] for r in results],
            ["Room A_B projector broken"],
        )

    def test_backslash_literal(self):
        results = database.get_reports(
            keyword=r"C:\temp", db_path=self.db_path
        )
        self.assertEqual(
            [r["title"] for r in results],
            [r"Path C:\temp unavailable"],
        )


if __name__ == "__main__":
    unittest.main()
