"""
CampusFix - Database Module
Agile Team Project - SE_CampusFix_Team04
National Taipei University / Software Engineering

Handles SQLite database initialization, report creation, queries,
filtering, and status updates with transaction safety.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'campusfix.db')

def get_connection(db_path=None):
    """Returns a connection to the SQLite database with dict-like row access."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=None):
    """Initializes the reports table if it doesn't already exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted',
            resolution_note TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def generate_report_id(conn):
    """
    Generates a unique human-friendly report ID (e.g. CF-1001, CF-1002).
    CF-12: Unique IDs for separate reports.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM reports")
    row = cursor.fetchone()
    next_id = (row[0] if row[0] is not None else 0) + 1
    return f"CF-{1000 + next_id}"

def create_report(title, location, category, description, db_path=None):
    """
    Saves a new report to the database.
    CF-10: Save title, location, category, description.
    CF-12: Generate unique report ID and default status 'Submitted'.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    report_id = generate_report_id(conn)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO reports (report_id, title, location, category, description, status, resolution_note, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'Submitted', '', ?, ?)
    """, (report_id, title.strip(), location.strip(), category.strip(), description.strip(), now, now))
    
    conn.commit()
    inserted_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM reports WHERE id = ?", (inserted_id,))
    report = dict(cursor.fetchone())
    conn.close()
    return report

def get_report_by_id(report_id_or_num, db_path=None):
    """Fetch a single report by its custom report_id (e.g. CF-1001) or primary key id."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    report_id_or_num = str(report_id_or_num).upper()
    if report_id_or_num.startswith("CF-"):
        cursor.execute("SELECT * FROM reports WHERE report_id = ?", (report_id_or_num,))
    else:
        cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id_or_num,))
        
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_reports(keyword=None, location=None, db_path=None):
    """
    Query reports with optional keyword search and location filter.
    Sprint 2 (CF-21):
      - Case-insensitive search on title and description.
      - Exact match on location.
      - Combined behavior: AND logic (matches keyword in title/desc AND matches location).
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    query = "SELECT * FROM reports WHERE 1=1"
    params = []
    
    if keyword and keyword.strip():
        escaped = keyword.strip().lower()
        escaped = escaped.replace("\\", "\\\\")
        escaped = escaped.replace("%", "\\%")
        escaped = escaped.replace("_", "\\_")
    
        k = f"%{escaped}%"
        query += (
            " AND (LOWER(title) LIKE ? ESCAPE '\\' "
            "OR LOWER(description) LIKE ? ESCAPE '\\')"
        )
        params.extend([k, k])

        
    if location and location.strip() and location != "All Locations":
        query += " AND location = ?"
        params.append(location.strip())
        
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_report_status(report_id_or_num, new_status, resolution_note="", db_path=None):
    """
    Updates the status and optional resolution note of a report.
    CF-30: Staff resolution management. Requires note when resolving.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_id_or_num = str(report_id_or_num).upper()
    if report_id_or_num.startswith("CF-"):
        query = "UPDATE reports SET status = ?, resolution_note = ?, updated_at = ? WHERE report_id = ?"
    else:
        query = "UPDATE reports SET status = ?, resolution_note = ?, updated_at = ? WHERE id = ?"
        
    cursor.execute(query, (new_status, resolution_note.strip(), now, report_id_or_num))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def reset_and_seed(db_path=None):
    """Seeds initial test data for demonstration purposes in pure English."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS reports")
    conn.commit()
    conn.close()
    
    init_db(db_path)
    
    sample_reports = [
        (
            "Projector bulb flickering in Room B102",
            "College of Business",
            "Classroom Equipment",
            "The ceiling projector keeps flickering off every 5 minutes during lecture.",
            "Submitted",
            ""
        ),
        (
            "Wi-Fi signal drops frequently in 3F study area",
            "Library",
            "Wi-Fi Failures",
            "NTPU-WiFi disconnects every 10 minutes near the east window tables on 3rd floor.",
            "In Progress",
            ""
        ),
        (
            "Restroom water dispenser leaking on 2F",
            "College of Law",
            "Damaged Facilities",
            "Water is dripping steadily onto the tile floor next to room L204, creating a slip hazard.",
            "Resolved",
            "Facility crew replaced the worn valve seal on Thursday morning. Floor dried and hazard warning sign removed."
        ),
        (
            "Air conditioning blowing hot air in Room 104",
            "College of Social Sciences",
            "Classroom Equipment",
            "Central AC unit seems stuck in fan mode, ambient temperature inside is over 28C.",
            "Submitted",
            ""
        ),
        (
            "Broken door handle on Computer Lab 3",
            "College of Electrical Engineering & Computer Science",
            "Damaged Facilities",
            "The exterior handle is loose and students get locked out if the door latches shut.",
            "In Progress",
            ""
        )
    ]
    
    for title, loc, cat, desc, status, res_note in sample_reports:
        conn = get_connection(db_path)
        r_id = generate_report_id(conn)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reports (report_id, title, location, category, description, status, resolution_note, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (r_id, title, loc, cat, desc, status, res_note, now, now))
        conn.commit()
        conn.close()
