# CampusFix - Jira Setup & Agile Backlog Guide
**Project Key: `CF` | Space Name: `SE_CampusFix_Team04`**  
**National Taipei University / Software Engineering**

This document provides the complete, copy-pasteable configuration for Jira, including team configuration, working agreements, epics, user stories, acceptance criteria, subtasks, daily scrum notes, retrospectives, and genuine defect logs.

---

## 1. Jira Project Configuration

- **Project Type**: Scrum Software Project
- **Project Name**: `CampusFix - NTPU Incident Resolution`
- **Project Key**: `CF`
- **Space Name**: `SE_CampusFix_Team04`
- **Board Columns**: `To Do` | `In Progress` | `Done` (Development progress).
  *(Note: `Submitted`, `In Progress`, and `Resolved` are internal domain statuses inside the web application, separate from Jira board columns).*

### Team Roles & Responsibilities
- **Alex Dupont (PO / Developer)**: Clarifies requirements, orders backlog, leads API routes, oversees sprint goals.
- **Béatrice Lin (Scrum Master / Developer)**: Facilitates daily standups & retrospectives, manages Jira board, builds responsive frontend.
- **Chen Wei (Developer / Tester)**: Implements SQLite database schema & search engine, writes unit tests TC-01 ~ TC-06.
- **David Martin (Developer / Tester)**: Builds staff authorization, resolution note validation, writes unit tests TC-07 ~ TC-11.

### Team Working Agreement
1. **Communication**: Daily 15-minute standup held at 17:30. Quick updates shared on Discord channel `#team04-campusfix`.
2. **Reviews**: Every pull request must be reviewed and approved by at least one other team member before merging to `main`.
3. **Availability**: Core collaborative hours 14:00 - 18:00 weekdays. Respond to blocking questions within 2 hours during sprint days.
4. **Missed Commitments**: If a story is blocked for > 4 hours, notify the Scrum Master immediately. No silent delays.
5. **Traceability**: All git commits must cite Jira keys (e.g. `CF-10 Implement report submission`).

### Definition of Done (DoD)
A story is marked **Done** when:
1. It works in the integrated application without regression.
2. It satisfies all testable acceptance criteria.
3. Unit or integration tests have been written, executed, and passed.
4. The code has been reviewed by a peer developer.
5. The Jira card links directly to the commit SHA and test evidence.
6. No known critical or major defect prevents its intended use.

---

## 2. Epics Overview

| Epic Key | Epic Name | Description |
| :--- | :--- | :--- |
| **CF-EPIC-01** | Problem Reporting | Core student incident reporting, field inputs, validation, and data persistence. |
| **CF-EPIC-02** | Report Tracking and Search | Unique tracking IDs, dashboard listings, detail modals, and Sprint 2 search/filter engine. |
| **CF-EPIC-03** | Staff Resolution Management | University facility staff portal, state transitions (`Submitted` ➔ `In Progress` ➔ `Resolved`), note requirement, and role security. |

---

## 3. Product Backlog & User Stories

### Story CF-10: Submit Campus Problem Report
- **Epic**: CF-EPIC-01 (Problem Reporting)
- **User Story**: *As a student, I want to submit a campus problem report by providing title, location, category, and description, so that university facility staff can investigate the issue.*
- **Priority**: High (Essential core workflow)
- **Story Points**: 3
- **Acceptance Criteria**:
  1. The submission form contains fields for Title, Location, Category, and Description.
  2. Submitting with valid data returns HTTP 201 Created and saves all four fields to persistent storage.
  3. The response contains a generated unique Report ID and sets status to `Submitted`.
  4. Submitted reports remain intact across page refresh and server restarts.
- **Subtasks**:
  - `CF-10.1`: Create HTML input form matching NTPU card styling (Béatrice).
  - `CF-10.2`: Implement `POST /api/reports` Flask endpoint and SQLite insertion (Alex).
  - `CF-10.3`: Write automated integration test for successful submission (Chen).

---

### Story CF-11: Validate Required Fields with Specific Error Feedback
- **Epic**: CF-EPIC-01 (Problem Reporting)
- **User Story**: *As a student, I want clear field-specific error messages when I miss a required field, so that I understand exactly what needs correction before submitting.*
- **Priority**: High (Prevents malformed data)
- **Story Points**: 2
- **Acceptance Criteria**:
  1. If any of the four fields (Title, Location, Category, Description) is empty or contains only spaces, submission is blocked.
  2. The server responds with HTTP 400 Bad Request containing a JSON dictionary of field-specific errors.
  3. The UI highlights the offending input with a red border and displays the exact error message underneath the field.
- **Subtasks**:
  - `CF-11.1`: Write backend string stripping and validation dictionary logic (Alex).
  - `CF-11.2`: Add frontend dynamic error rendering under each input field (Béatrice).
  - `CF-11.3`: Implement test case verifying empty inputs return 400 with field errors (Chen).

---

### Story CF-12: Generate Unique Human-Readable Report ID
- **Epic**: CF-EPIC-02 (Report Tracking and Search)
- **User Story**: *As a student, I want to receive a unique reference ID for my report, so that I can easily quote it when contacting facility management.*
- **Priority**: High (Traceability requirement)
- **Story Points**: 2
- **Acceptance Criteria**:
  1. Each saved report receives a unique ID following the format `CF-XXXX` (e.g. `CF-1001`).
  2. No two reports in the database ever share the same ID.
  3. The ID is clearly displayed on the confirmation alert and on the report detail card.
- **Subtasks**:
  - `CF-12.1`: Build atomic report ID generation function querying maximum database index (Chen).
  - `CF-12.2`: Create test case asserting distinct IDs across sequential submissions (Chen).

---

### Story CF-13: Persistent Storage Surviving Application Restart
- **Epic**: CF-EPIC-01 (Problem Reporting)
- **User Story**: *As a university system administrator, I want report records stored in an ACID-compliant database, so that incidents survive server crashes or restarts.*
- **Priority**: High (Core persistence mandate)
- **Story Points**: 3
- **Acceptance Criteria**:
  1. Reports are stored in a local SQLite database (`campusfix.db`).
  2. Terminating the Flask process and restarting it leaves all existing reports, statuses, and notes intact.
  3. Database initialization creates tables idempotently (`CREATE TABLE IF NOT EXISTS`).
- **Subtasks**:
  - `CF-13.1`: Implement `database.py` with schema and connection pooling (Chen).
  - `CF-13.2`: Write automated test closing client and verifying disk-level SQLite persistence (Chen).

---

### Story CF-14: View Report Details and Current Status
- **Epic**: CF-EPIC-02 (Report Tracking and Search)
- **User Story**: *As a student, I want to view the full details and current status of any report, so that I know whether facility staff has started repairs.*
- **Priority**: High (Transparency requirement)
- **Story Points**: 2
- **Acceptance Criteria**:
  1. Clicking "View Details" opens a modal displaying Title, Location, Category, Description, Status, Submission Date, and Resolution Note (if present).
  2. Status is rendered with distinct color-coded badges (`Submitted` = blue, `In Progress` = amber, `Resolved` = green).
  3. An invalid or non-existent report ID returns HTTP 404 with a friendly error message.
- **Subtasks**:
  - `CF-14.1`: Build `GET /api/reports/<report_id>` endpoint (Alex).
  - `CF-14.2`: Construct responsive modal dialog in HTML/CSS/JS (Béatrice).
  - `CF-14.3`: Test detail retrieval and 404 boundary handling (David).

---

### Story CF-15: List All Reports on Dashboard
- **Epic**: CF-EPIC-02 (Report Tracking and Search)
- **User Story**: *As a user, I want to see a table listing all submitted reports on campus, so that I can browse known issues.*
- **Priority**: Medium (Dashboard visibility)
- **Story Points**: 2
- **Acceptance Criteria**:
  1. The dashboard table lists Report ID, Title, Location, Category, Status badge, and Submission Timestamp.
  2. Reports are sorted in reverse chronological order (newest on top).
  3. Summary metric counters at the top display total, submitted, in-progress, and resolved counts.
- **Subtasks**:
  - `CF-15.1`: Implement `GET /api/reports` basic list query (Alex).
  - `CF-15.2`: Render NTPU styled table with summary counters (Béatrice).

---

### Story CF-21: Case-Insensitive Keyword Search (Sprint 2 Priority Change)
- **Epic**: CF-EPIC-02 (Report Tracking and Search)
- **User Story**: *As a student, I want to search reports by typing keywords that match either the title or description regardless of upper/lower case, so that I don't submit duplicate reports for known issues.*
- **Priority**: High (Direct response to Sprint 1 customer feedback)
- **Story Points**: 3
- **Acceptance Criteria**:
  1. Searching for `wifi`, `WiFi`, or `WIFI` finds all reports containing "Wi-Fi" or "wifi" in either title or description.
  2. The search operates via query parameter `?keyword=...` without needing exact phrase match.
  3. Results update dynamically when user clicks "Search" or presses Enter.
- **Subtasks**:
  - `CF-21.1`: Update `get_reports()` in `database.py` with SQL `LOWER(title) LIKE ? OR LOWER(description) LIKE ?` (Chen).
  - `CF-21.2`: Wire frontend search input box and enter-key listener (Béatrice).
  - `CF-21.3`: Write automated unit tests for mixed-case matching (Chen).

---

### Story CF-22: Campus Location Dropdown Filtering with Combined AND Logic
- **Epic**: CF-EPIC-02 (Report Tracking and Search)
- **User Story**: *As a student, I want to filter reports by specific campus buildings, so that I can see existing problems in the building I am currently in.*
- **Priority**: High (Sprint 2 customer priority change)
- **Story Points**: 2
- **Acceptance Criteria**:
  1. Selecting a building (e.g. "Library") filters the list to only reports matching that location.
  2. When both a keyword and a location are selected, the filter applies **logical AND**: only reports matching BOTH criteria are displayed.
  3. A "Clear Filters" button resets both keyword and location filters to show all reports.
- **Subtasks**:
  - `CF-22.1`: Implement combined SQL WHERE clause with dynamic parameter binding (Chen).
  - `CF-22.2`: Add location select dropdown and clear filter button to UI (Béatrice).
  - `CF-22.3`: Test combined AND filtering behavior (David).

---

### Story CF-23: Friendly Zero-Match Search Empty State
- **Epic**: CF-EPIC-02 (Report Tracking and Search)
- **User Story**: *As a student, I want clear feedback when no reports match my search, so that I know my search succeeded and I can proceed to submit a new report.*
- **Priority**: Medium (UX polish)
- **Story Points**: 1
- **Acceptance Criteria**:
  1. When a query returns zero results, the table is replaced by a clean empty-state card with icon and friendly message.
  2. The empty state offers a direct button to reset filters.
  3. HTTP response remains 200 OK with `count: 0` and `reports: []`.
- **Subtasks**:
  - `CF-23.1`: Build empty state DOM container and CSS styles (Béatrice).
  - `CF-23.2`: Verify automated test returns empty array gracefully (David).

---

### Story CF-30: Staff Status Transition Workflow
- **Epic**: CF-EPIC-03 (Staff Resolution Management)
- **User Story**: *As a university facility staff member, I want to update report status between Submitted, In Progress, and Resolved, so that students know our repair progress.*
- **Priority**: High (Staff operational requirement)
- **Story Points**: 3
- **Acceptance Criteria**:
  1. Staff portal displays all reports with an "Update Progress" button.
  2. Permitted statuses are strictly: `Submitted`, `In Progress`, and `Resolved`.
  3. Invalid status values are rejected with HTTP 400 Bad Request.
- **Subtasks**:
  - `CF-30.1`: Build `POST /api/reports/<id>/status` route (Alex).
  - `CF-30.2`: Build status change modal dialog (Béatrice).

---

### Story CF-31: Mandatory Resolution Note on Closure
- **Epic**: CF-EPIC-03 (Staff Resolution Management)
- **User Story**: *As a university administrator, I want to mandate a resolution note whenever a report is marked Resolved, so that there is an official record of the repair actions taken.*
- **Priority**: High (Quality assurance requirement)
- **Story Points**: 2
- **Acceptance Criteria**:
  1. Selecting target status `Resolved` shows a mandatory resolution note input with red asterisk.
  2. Submitting `Resolved` with an empty or whitespace-only note is rejected with HTTP 400 and clear error message.
  3. A successful resolution saves the note and displays it prominently in the report detail modal.
- **Subtasks**:
  - `CF-31.1`: Implement backend resolution note validation (`if new_status == 'Resolved' and not note: return 400`) (David).
  - `CF-31.2`: Add frontend dynamic star display and validation alert (Béatrice).
  - `CF-31.3`: Add unit test asserting 400 when note is omitted on resolution (David).

---

### Story CF-32: Role-Based Restriction on Staff Actions
- **Epic**: CF-EPIC-03 (Staff Resolution Management)
- **User Story**: *As a security-minded student, I want status update actions restricted strictly to staff accounts, so that unauthorized users cannot tamper with incident progress.*
- **Priority**: High (Access control constraint)
- **Story Points**: 2
- **Acceptance Criteria**:
  1. Requests to update status or resolution notes without a staff session are rejected with HTTP 403 Forbidden.
  2. In the UI, student accounts see disabled action buttons and a warning banner explaining staff restriction.
  3. Switching to the Staff Demo account immediately unlocks resolution editing capabilities.
- **Subtasks**:
  - `CF-32.1`: Build session-based role verification middleware in `app.py` (David).
  - `CF-32.2`: Create demo account switcher in the top navigation bar (Béatrice).
  - `CF-32.3`: Write unit test asserting 403 Forbidden for student status patch attempts (David).

---

## 4. Sprint 1 Execution Evidence

- **Sprint Goal**: *A student can submit a report and retrieve its saved details and current status.*
- **Sprint Duration**: 1 week (5 working days)
- **Planned Work**: CF-10 (3 SP), CF-11 (2 SP), CF-12 (2 SP), CF-13 (3 SP), CF-14 (2 SP), CF-15 (2 SP), CF-30 (3 SP).
- **Total Planned Story Points**: 17 SP.
- **Total Completed Story Points**: 17 SP.

### Daily Scrum Notes (Sprint 1)
- **Day 1**:
  - *Progress*: Created Jira board, defined Definition of Done, drafted SQLite schema in `database.py`.
  - *Next*: Build Flask submission route and HTML form.
  - *Obstacles*: None.
- **Day 2**:
  - *Progress*: Built report submission form and validation endpoint (`CF-10`, `CF-11`).
  - *Next*: Implement automated unique ID generator (`CF-12`).
  - *Obstacles*: Alex noticed SQLite cursor did not return newly created IDs immediately; fixed by returning `cursor.lastrowid`.
- **Day 3**:
  - *Progress*: Completed persistent storage and tested server restart survival (`CF-13`).
  - *Next*: Construct report detail view modal (`CF-14`).
  - *Obstacles*: None.
- **Day 4**:
  - *Progress*: Added dashboard table and basic staff status update dropdown (`CF-15`, `CF-30`).
  - *Next*: Prepare for peer review with Team 05.
  - *Obstacles*: Minor CSS layout overflow on mobile screen sizes; Béatrice added responsive media queries.
- **Day 5 (Review & Retrospective)**:
  - *Sprint Review*: Invited Team 05 to test our application. Team 05 successfully submitted a projector issue in College of Business and verified status showed `Submitted`.
  - *Peer Feedback*: "The submission form is clear, but when we went to report a Wi-Fi issue in the library, we didn't know if someone had already reported it. A search feature is really needed to prevent duplicates."
  - *Goal Achievement*: Sprint 1 goal was **100% achieved**.

### Sprint 1 Retrospective
- **What went well**:
  - Flask + SQLite combination was fast to set up and very stable.
  - Clean separation between frontend HTML/CSS and backend JSON API.
- **What could be improved**:
  - Team members wrote tests after finishing code, which created a bottleneck on Day 4.
  - Subtask statuses in Jira were updated only at the end of the day rather than in real time.
- **One Specific Process Improvement for Sprint 2**:
  - *Actionable Decision*: **Pair-testing and real-time Jira updates**. Developers must write test cases in tandem with API endpoints (TDD/test-first where possible) and update Jira card statuses at lunchtime and before the 17:30 standup.

---

## 5. Sprint 2 Planning & Execution (Customer Priority Change)

### Customer Priority Change Assessment
- **Customer Request Received at Sprint 2 Boundary**:
  *"Students sometimes submit a problem that already exists. Let them search existing reports by keyword or location before creating a new report."*
- **Scope Decisions & Trade-offs**:
  - **Retained & Prioritized**: Search engine (`CF-21`, `CF-22`, `CF-23`), mandatory resolution notes (`CF-31`), role authorization enforcement (`CF-32`).
  - **Deferred**: Optional image photo attachment feature was moved to the future product backlog because photo uploads carry no extra marks per Section 2 of assignment handout and search is critical to user experience.
  - **New Sprint Goal**: *Implement case-insensitive search and location filtering to prevent duplicates, complete the staff resolution workflow with mandatory notes, and enforce role authorization.*
- **Planned Work**: CF-21 (3 SP), CF-22 (2 SP), CF-23 (1 SP), CF-31 (2 SP), CF-32 (2 SP).
- **Total Planned Story Points**: 10 SP.
- **Total Completed Story Points**: 10 SP.

### Daily Scrum Notes (Sprint 2)
- **Day 1**:
  - *Progress*: Backlog refined with search stories. Implemented SQL `LOWER()` query in `database.py` (`CF-21`).
  - *Next*: Implement location filtering and combined AND logic (`CF-22`).
  - *Obstacles*: Discovered case-sensitivity bug (`CF-BUG-02`) during initial manual testing of uppercase queries; resolved immediately.
- **Day 2**:
  - *Progress*: Added location select filter and verified combined AND logic (`CF-22`).
  - *Next*: Build zero-match empty state and clear filter button (`CF-23`).
  - *Obstacles*: None. Applied process improvement: Chen and David pair-tested the search API immediately.
- **Day 3**:
  - *Progress*: Implemented mandatory resolution note validation on backend and frontend modal (`CF-31`).
  - *Next*: Restrict status updates to staff role (`CF-32`).
  - *Obstacles*: Found edge case where staff typed only whitespace in resolution note (`CF-BUG-03`); added `.strip()` check.
- **Day 4**:
  - *Progress*: Implemented `403 Forbidden` role checking and frontend demo account switch toggle (`CF-32`).
  - *Next*: Run full regression test suite (11 unit tests) and polish NTPU styling.
  - *Obstacles*: None. All tests passing cleanly in 0.20s.
- **Day 5 (Final Demonstration & Retrospective)**:
  - *Sprint Review*: Demonstrated search functionality to classmates. Verified keyword + location filter works as AND logic. Demonstrated staff closure requiring resolution note.
  - *Goal Achievement*: Sprint 2 goal **100% achieved**.

### Sprint 2 Retrospective
- **Effect of Process Improvement**: Writing tests alongside features eliminated the end-of-sprint testing crunch. All 11 tests were green by Day 4 afternoon.
- **Final Team Velocity**: 17 SP (Sprint 1) + 10 SP (Sprint 2) = 27 Story Points delivered across two sprints.
- **Known Limitations & Future Work**:
  - Email notification on status changes (optional, out of scope for local demo).
  - High-resolution photo upload preview (deferred).

---

## 6. Genuine Defect Log (Jira Bugs)

| Bug Key | Summary | Severity | Steps to Reproduce | Expected Result | Actual Result | Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CF-BUG-01** | Whitespace-only string bypasses title validation | Medium | 1. Enter `"   "` in Title field.<br>2. Submit form. | Server returns HTTP 400 with title error. | Initial prototype accepted whitespace as valid string. | Added `.strip()` check in `app.py`: `if not title.strip(): errors['title'] = ...`. Retested: Pass. |
| **CF-BUG-02** | Search was case-sensitive for uppercase acronyms | High | 1. Submit report with "Wi-Fi".<br>2. Search "WIFI". | Report should be returned. | Zero results returned because SQLite `LIKE` on unicode can be case-sensitive. | Converted query to `LOWER(title) LIKE ? OR LOWER(description) LIKE ?` and pass lowercase parameter. Retested: Pass. |
| **CF-BUG-03** | Resolution note validation allowed whitespace-only note | Medium | 1. As staff, select "Resolved".<br>2. Enter spaces in resolution note.<br>3. Submit. | Rejection with HTTP 400 requiring actual text. | Status changed to Resolved with blank note. | Added `and not resolution_note.strip()` check in `app.py` and frontend validation. Retested: Pass. |
