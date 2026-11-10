# CampusFix - 7-Minute Team Demonstration Script
**National Taipei University / Software Engineering (Team 04)**  
**Demonstrators**: Alex Dupont, Béatrice Lin, Chen Wei, David Martin

---

## Time Allocation Overview (Strict 7 Minutes Total)
- **Part 1 (0:00 - 4:00 | 4 Minutes)**: Live Application Demonstration (Submit, Retrieve, Search, Resolve, Validation, Persistence).
- **Part 2 (4:00 - 7:00 | 3 Minutes)**: Trace One Story (`CF-21`: Case-Insensitive Search) across Jira, Code, Tests, and Q&A.

---

### Part 1: Live Application Demonstration (4 Minutes)

#### [0:00 - 0:45] Introduction & NTPU Theme Context (Speaker: Béatrice Lin)
- *"Hello Professor and classmates. We are Team 04, and this is CampusFix, an agile problem reporting and tracking platform designed for National Taipei University."*
- Point out the UI styling: *"As you can see, our UI adheres to NTPU's official design system at `new.ntpu.edu.tw`—featuring NTPU deep blue `#003366`, gold emblem accents, top accessibility navigation (`::: Skip to main content`), and clear status badges."*
- Point to top right: *"Per course specifications, demonstration accounts are built-in: we are currently logged in as Student Demo (`student@ntpu.edu.tw`)."*

#### [0:45 - 1:45] Validation & Submitting a Problem Report (Speaker: Alex Dupont)
- Click tab: **Report a Problem**.
- Demonstrate validation:
  - Leave fields blank and click "Submit Problem Report".
  - *"Notice that submission is blocked immediately. Clear red borders and field-specific error messages highlight that Title, Location, Category, and Description are all mandatory."*
- Submit a valid report:
  - Title: `College of Business Room B102 Projector flickering`
  - Location: `College of Business`
  - Category: `Classroom Equipment`
  - Description: `Projector lamp shuts down every 5 minutes during lecture.`
  - Click Submit.
  - *"The server returns HTTP 201 Created and generates unique ID CF-1006 with initial status 'Submitted'."*
  - Pop up details modal to show all saved fields.

#### [1:45 - 2:30] Data Persistence Across Server Restart (Speaker: Chen Wei)
- *"Now we will prove persistence: data must survive a page refresh and application restart."*
- Refresh the browser page: *"All data remains intact."*
- Switch to terminal: Press `Ctrl+C` to terminate `python app.py`. Restart it: `python app.py`.
- Refresh browser: *"Our SQLite database `campusfix.db` reliably preserves all reports across application restarts."*

#### [2:30 - 3:15] Sprint 2 Search & Location Filtering (Speaker: Alex Dupont)
- Navigate to: **Search & Track Reports**.
- Demonstrate case-insensitive keyword search:
  - Type `wifi` in search box and click Search.
  - *"Even though the report in our database was stored as 'Wi-Fi' with capital letters and hyphen, searching lowercase 'wifi' finds it immediately."*
  - Type uppercase `WIFI` or description keyword `reading room`: *"Matched accurately."*
- Demonstrate combined location filter (AND logic):
  - Select Location: `Library`.
  - *"When both keyword and location are provided, CampusFix applies logical AND: it filters for issues containing 'wifi' located in the Library."*
- Demonstrate empty state:
  - Type `nonexistent_xyz` -> shows friendly empty state card with clear instructions to reset filters.

#### [3:15 - 4:00] Staff Resolution Workflow & Role Security (Speaker: David Martin)
- Switch to: **Staff Management Portal**.
- Show security restriction as student:
  - *"Because we are currently logged in as a student, notice the warning banner: status modification buttons are disabled. If a student tries to send a status update via API, our server responds with HTTP 403 Forbidden."*
- Switch role in top header: Click **Switch to Staff Account**.
  - *"We are now authenticated as Staff Demo (`staff@ntpu.edu.tw`)."*
- Click **Update Progress** on `CF-1006`:
  - Select status: `Resolved`.
  - Notice the mandatory red asterisk appears: *"If we try to save without a resolution note, the system prevents it with an error."*
  - Enter resolution note: `Facility team replaced the projector lamp on Friday. Tested with HDMI input; display is steady.`
  - Click "Save Status Update".
  - *"Status instantly updates to 'Resolved' with green badge, and the resolution note is permanently recorded."*

---

### Part 2: Tracing One Story Across Jira, Code & Tests (3 Minutes)

#### [4:00 - 5:00] Story in Jira Backlog: `CF-21` (Speaker: Béatrice Lin)
- Open Jira Board:
  - *"We will now trace Story **CF-21**: Case-Insensitive Keyword Search."*
  - *"In Jira space `SE_CampusFix_Team04`, this story was created at the Sprint 2 boundary in response to customer feedback requesting search before submission to prevent duplicates."*
  - Read acceptance criteria:
    1. Case-insensitive search on title and description.
    2. Dynamic updates via query parameters.
    3. Integration with Definition of Done.
  - *"Estimated at 3 Story Points; completed and verified with commit key CF-21."*

#### [5:00 - 6:00] Code Trace in `app.py` & `database.py` (Speaker: Chen Wei)
- Open code editor:
  - Show Flask endpoint in `app.py`:
    ```python
    @app.route('/api/reports', methods=['GET'])
    def list_reports():
        keyword = request.args.get('keyword', '').strip()
        location = request.args.get('location', '').strip()
        reports = get_reports(keyword=keyword, location=location)
        return jsonify({'success': True, 'count': len(reports), 'reports': reports})
    ```
  - Show database query in `database.py`:
    ```python
    if keyword and keyword.strip():
        k = f"%{keyword.strip().lower()}%"
        query += " AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?)"
        params.extend([k, k])
    ```
  - *"Here we convert both columns and search parameter to lowercase, guaranteeing case-insensitive matching in SQLite."*

#### [6:00 - 6:45] Automated Test Verification (Speaker: David Martin)
- Open terminal and show test `test_06_keyword_search_case_insensitive` in `tests/test_campusfix.py`:
  - Run tests:
    ```bash
    python -m unittest discover -s tests -p "test_*.py"
    ```
  - Point to terminal output:
    ```text
    ...........
    Ran 11 tests in 0.200s
    OK
    ```
  - *"All 11 tests pass in 0.20 seconds, confirming that CF-21 passes all acceptance criteria and satisfies our Definition of Done."*

#### [6:45 - 7:00] Wrap-up & Q&A
- *"CampusFix was delivered on time through two sprints, with 27 story points completed and zero known critical defects. Thank you, and we welcome any questions!"*
