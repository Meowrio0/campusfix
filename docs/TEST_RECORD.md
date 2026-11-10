# CampusFix - Official Test Record & Evidence
**National Taipei University / Software Engineering**  
**Team: SE_CampusFix_Team04**  
**Automated Test Suite**: `tests/test_campusfix.py` (11 Tests Passing in 0.20s)

---

## 1. Test Coverage Matrix

This document provides formal test records covering all 10 required test cases specified in Section 10 of the assignment handout, plus 1 additional regression test verifying combined filter logic.

| Test ID | Coverage Area | Related Story | Tester | Automated Test Method | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Valid report submission | CF-10 | Chen Wei | `test_01_valid_report_submission` | **PASS** |
| **TC-02** | Missing required field | CF-11 | Chen Wei | `test_02_missing_required_field` | **PASS** |
| **TC-03** | Unique IDs for separate reports | CF-12 | Chen Wei | `test_03_unique_ids_for_separate_reports` | **PASS** |
| **TC-04** | Persistence after refresh and restart | CF-13 | Chen Wei | `test_04_persistence_after_restart` | **PASS** |
| **TC-05** | Correct report details and status | CF-14 | David Martin | `test_05_correct_report_details_and_status` | **PASS** |
| **TC-06** | Keyword search, including different letter case | CF-21 | Chen Wei | `test_06_keyword_search_case_insensitive` | **PASS** |
| **TC-07** | Location filtering | CF-22 | David Martin | `test_07_location_filtering` | **PASS** |
| **TC-08** | Search with no matches | CF-23 | David Martin | `test_08_search_with_no_matches` | **PASS** |
| **TC-09** | Staff update and required resolution note | CF-31 | David Martin | `test_09_staff_update_and_required_resolution_note` | **PASS** |
| **TC-10** | Student prevented from staff update actions | CF-32 | David Martin | `test_10_student_prevented_from_staff_update_actions` | **PASS** |
| **TC-11** | Combined filters (Keyword AND Location logic) | CF-22 | Alex Dupont | `test_11_combined_filters_and_logic` | **PASS** |

---

## 2. Detailed Test Cases & Execution Results

### Test Case TC-01: Valid Report Submission
- **Related Story Key**: `CF-10`
- **Tester**: Chen Wei
- **Test Objective**: Verify that submitting a complete, valid form saves all fields and generates a report with status `Submitted`.
- **Preconditions**: Application running; database initialized.
- **Steps / Input**:
  1. Navigate to the submission form ("Report a Problem").
  2. Input Title: `"Broken HDMI cable in Room 301"`.
  3. Select Location: `"College of Business"`.
  4. Select Category: `"Classroom Equipment"`.
  5. Input Description: `"HDMI cable at the lectern has bent pins and cannot connect to laptop."`.
  6. Click "Submit Problem Report".
- **Expected Result**: HTTP 201 Created. Response contains generated report ID (e.g. `CF-1006`), status `Submitted`, and matches all inputs.
- **Actual Result**: HTTP 201 received. Report `CF-1006` saved with status `Submitted` and displayed in success banner.
- **Outcome**: **PASS**

---

### Test Case TC-02: Missing Required Field
- **Related Story Key**: `CF-11`
- **Tester**: Chen Wei
- **Test Objective**: Verify that submitting with missing or blank fields is blocked and displays specific error messages.
- **Steps / Input**:
  1. Open submission form.
  2. Leave Title blank (`"   "`).
  3. Select Location: `"Library"`.
  4. Select Category: `"Wi-Fi Failures"`.
  5. Leave Description empty (`""`).
  6. Click Submit.
- **Expected Result**: HTTP 400 Bad Request. Response contains errors dictionary identifying `title` and `description`. UI displays red borders and field-specific error messages.
- **Actual Result**: HTTP 400 returned with `{errors: {title: "Title is required...", description: "Problem description is required."}}`. Submission rejected.
- **Outcome**: **PASS**

---

### Test Case TC-03: Unique IDs for Separate Reports
- **Related Story Key**: `CF-12`
- **Tester**: Chen Wei
- **Test Objective**: Verify consecutive submissions receive distinct, monotonically unique report IDs.
- **Steps / Input**:
  1. Submit Report A: Title `"Broken window blind"`, Location `"Library"`.
  2. Submit Report B: Title `"Restroom tap leaking"`, Location `"College of Law"`.
  3. Compare returned `report_id` fields.
- **Expected Result**: Report A receives ID (e.g. `CF-1007`), Report B receives ID (e.g. `CF-1008`). IDs are non-identical.
- **Actual Result**: `CF-1007` != `CF-1008`. Primary key IDs are distinct.
- **Outcome**: **PASS**

---

### Test Case TC-04: Persistence After Refresh and Restart
- **Related Story Key**: `CF-13`
- **Tester**: Chen Wei
- **Test Objective**: Confirm that reports stored in SQLite persist after restarting the backend server.
- **Steps / Input**:
  1. Submit a report `"Persistent projector issue"` via API.
  2. Note returned ID (`CF-1009`).
  3. Terminate Flask server process (close Python session).
  4. Start fresh server process and query database directly via SQLite engine.
- **Expected Result**: Report `CF-1009` is retrieved with original title, description, and status intact.
- **Actual Result**: Data survived process termination completely. SQLite file `campusfix.db` contains identical record.
- **Outcome**: **PASS**

---

### Test Case TC-05: Correct Report Details and Status
- **Related Story Key**: `CF-14`
- **Tester**: David Martin
- **Test Objective**: Verify `GET /api/reports/<id>` returns comprehensive, accurate fields and timestamps.
- **Steps / Input**:
  1. Request `GET /api/reports/CF-1001`.
  2. Inspect response JSON payload.
- **Expected Result**: Response 200 OK. Contains `report_id`, `title`, `location`, `category`, `description`, `status`, `resolution_note`, `created_at`, `updated_at`.
- **Actual Result**: All 8 domain fields present and match expected initial values.
- **Outcome**: **PASS**

---

### Test Case TC-06: Keyword Search, Including Different Letter Case
- **Related Story Key**: `CF-21`
- **Tester**: Chen Wei
- **Test Objective**: Confirm keyword search finds matches in both title and description regardless of letter casing.
- **Steps / Input**:
  1. Database contains report: `"Eduroam Wi-Fi Disconnection"` with description `"Laptops lose connection on the 4th floor."`.
  2. Query 1: `GET /api/reports?keyword=wi-fi` (lowercase).
  3. Query 2: `GET /api/reports?keyword=WI-FI` (uppercase).
  4. Query 3: `GET /api/reports?keyword=4TH%20FLOOR` (uppercase query matching lowercase description).
- **Expected Result**: All three queries successfully return the targeted report record.
- **Actual Result**: Queries returned 1 record each. Case-insensitivity confirmed via `LOWER()` SQL matching.
- **Outcome**: **PASS**

---

### Test Case TC-07: Location Filtering
- **Related Story Key**: `CF-22`
- **Tester**: David Martin
- **Test Objective**: Verify dropdown location filter isolates reports belonging to the selected campus building.
- **Steps / Input**:
  1. Have 1 report in `"Library"` and 1 in `"College of Business"`.
  2. Send request: `GET /api/reports?location=Library`.
- **Expected Result**: Only the Library report is returned; College of Business report is excluded.
- **Actual Result**: Exactly 1 report returned with `location == "Library"`.
- **Outcome**: **PASS**

---

### Test Case TC-08: Search with No Matches
- **Related Story Key**: `CF-23`
- **Tester**: David Martin
- **Test Objective**: Verify querying an unmatched string returns an empty array cleanly without server error.
- **Steps / Input**:
  1. Send request: `GET /api/reports?keyword=nonexistent_xyz_query`.
- **Expected Result**: HTTP 200 OK, `count: 0`, `reports: []`. UI displays empty state notice.
- **Actual Result**: HTTP 200 returned with empty list. UI shows "No Reports Found".
- **Outcome**: **PASS**

---

### Test Case TC-09: Staff Update and Required Resolution Note
- **Related Story Key**: `CF-31`
- **Tester**: David Martin
- **Test Objective**: Confirm that staff can update status, but updating to `Resolved` strictly enforces a non-empty resolution note.
- **Steps / Input**:
  1. Authenticate session as staff (`role = 'staff'`).
  2. Send status update to `"Resolved"` with empty note: `POST /api/reports/CF-1001/status` with `resolution_note: "   "`.
  3. Verify rejection.
  4. Send valid resolution note: `"Replaced thermostat sensor and recharged refrigerant. Verified 23C."`.
- **Expected Result**: Step 2 fails with HTTP 400 Bad Request ("A resolution note is required..."). Step 4 succeeds with HTTP 200 OK and status updated to `Resolved`.
- **Actual Result**: Step 2 rejected with 400. Step 4 succeeded with 200 and note saved to SQLite.
- **Outcome**: **PASS**

---

### Test Case TC-10: Student Prevented from Staff Update Actions
- **Related Story Key**: `CF-32`
- **Tester**: David Martin
- **Test Objective**: Ensure a student user cannot modify report statuses.
- **Steps / Input**:
  1. Authenticate session as student (`role = 'student'`).
  2. Send status update: `POST /api/reports/CF-1001/status` with `status: "In Progress"`.
- **Expected Result**: HTTP 403 Forbidden. JSON response `{success: false, error: "Access denied: Only university staff..."}`.
- **Actual Result**: HTTP 403 returned. Database record unchanged.
- **Outcome**: **PASS**

---

### Test Case TC-11: Combined Filters (Keyword AND Location Logic)
- **Related Story Key**: `CF-22`
- **Tester**: Alex Dupont
- **Test Objective**: Verify the behavior of combined search criteria.
- **Rule**: When both keyword and location are provided, they must behave as **logical AND**: `(title MATCH OR desc MATCH) AND location MATCH`.
- **Steps / Input**:
  1. Database has:
     - Report 1: Title `"Projector broken"`, Location `"Library"`.
     - Report 2: Title `"Projector broken"`, Location `"College of Business"`.
  2. Send query: `GET /api/reports?keyword=Projector&location=Library`.
- **Expected Result**: Only Report 1 is returned (matches "Projector" AND matches "Library").
- **Actual Result**: Exactly 1 report returned (Report 1).
- **Outcome**: **PASS**

---

## 3. Automated Test Execution Output

```text
C:\Users\phone\.gemini\antigravity\scratch\campusfix> python -m unittest discover -s tests -p "test_*.py"
...........
----------------------------------------------------------------------
Ran 11 tests in 0.200s

OK
```

All 11 automated test cases executed cleanly, verifying data persistence, boundary checks, case-insensitive query matching, role-based authorization, and required resolution notes.
