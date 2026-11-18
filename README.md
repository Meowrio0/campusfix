# CampusFix - National Taipei University (NTPU) Problem Resolution System
**Software Engineering Course | Team Project | SE_CampusFix_Team04**

CampusFix is a lightweight campus incident and facility problem reporting web application built for National Taipei University. It empowers students to report physical campus defects (classroom projectors, Wi-Fi outages, plumbing leaks, etc.), tracks live resolution progress, enables case-insensitive search and filtering to avoid duplicate submissions, and provides a staff workflow with mandatory resolution notes.

The user interface follows the official visual identity of the [NTPU Portal](https://new.ntpu.edu.tw/), utilizing Taipei Tech/NTPU deep blue (`#003366`), gold accents (`#C5A059`), card containers, accessibility markers (`::: Skip to main content`), and clean responsive tables.

---

## Team Members & Roles (Team 04)

| Name | GitHub | Role | Part | Primary Responsibilities |
| :--- | :--- | :--- | :--- | :--- |
| **LI (Chu)** | `chu91014` | Product Owner / Developer | Part C | Backlog management & prioritization, Keyword/location search, SQL wildcard escaping (`CF-11`, `CF-12`, `CF-20`), Tests `TC-06` ~ `TC-08` |
| **王柏森 (Wang Baisen)** | `standardiuys` | Scrum Master / Developer | Part B | Scrum facilitation, Jira sprint & retro management, Unique report IDs & case-insensitive ID lookup (`CF-6`, `CF-9`, `CF-19`), Tests `TC-03`, `TC-05` |
| **林健勛 (Lin Jianxun)** | `Meowrio0` | Developer / Tester | Part A | GitHub repository setup & team coordination, Report submission & title length validation (`CF-5`, `CF-18`), Tests `TC-01`, `TC-02` |
| **Louis Imbert** | `Louis-ibt` | Developer / Tester | Part D | Staff role password authentication & SQLite persistence (`CF-7`, `CF-15`, `CF-21`), Tests `TC-04`, `TC-10` |
| **Axel Bauer** | `Axel_Algo` | Developer / Tester | Part E | Staff status updates, mandatory resolution notes & demo reset guard (`CF-13`, `CF-14`, `CF-17`, `CF-22`), Test `TC-09` |

---

## Quick Start Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- `pip` package manager

### 1. Installation
Clone the repository and install dependencies (Flask):
```bash
# Navigate to the project directory
cd campusfix

# Install Flask if not already installed
pip install flask
```

### 2. Run the Application
Switching to the staff account requires a password (Part D, CF-15). The password is **not stored in the repository**: the server reads it from the `CAMPUSFIX_STAFF_PASSWORD` environment variable, so set it before starting the app (choose any value):

```bash
# macOS / Linux / Git Bash
export CAMPUSFIX_STAFF_PASSWORD="choose-a-password"
python app.py
```
```powershell
# Windows PowerShell
$env:CAMPUSFIX_STAFF_PASSWORD = "choose-a-password"
python app.py
```
```bat
:: Windows Command Prompt (cmd)
set CAMPUSFIX_STAFF_PASSWORD=choose-a-password
python app.py
```

If the variable is not set, the app still runs, but switching to staff is refused for everyone (HTTP 403).

Open your web browser and navigate to:
👉 **`http://127.0.0.1:5000`**

The database (`campusfix.db`) initializes automatically with realistic NTPU campus reports.

### 3. Run Automated Tests
Execute the comprehensive test suite covering all required test cases and regression tests:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## Demonstration Accounts

As specified in the assignment handout, predefined demonstration accounts are provided. Use the **Switch Role** button at the top right of the navigation bar. Switching to staff asks for the staff password (the value of `CAMPUSFIX_STAFF_PASSWORD`, see Quick Start step 2); switching back to student needs no password:

1. **Student Account (`student@ntpu.edu.tw`)**:
   - Role: `student`
   - Permissions: Can submit new problem reports, search existing reports, view report details.
   - Restricted: Cannot modify report status, write resolution notes, or reset the demo database (server returns `403 Forbidden` if attempted).

2. **Staff Account (`staff@ntpu.edu.tw`)**:
   - Role: `staff` (Office of General Affairs / Facility Division)
   - Access: requires the staff password. A missing or wrong password is refused (`403 Forbidden`) and the account stays student.
   - Permissions: Can review all incoming reports, change status (`Submitted` ➔ `In Progress` ➔ `Resolved`), provide mandatory resolution notes upon closing an issue, and reset demo data.

---

## Features Delivered Across Sprints

### Sprint 1: Deliver Basic Workflow
- [x] **CF-5**: Problem report submission form (Title, Location, Category, Description) with strict field validation and 100-character title limit (**CF-18**).
- [x] **CF-6**: Automated generation of unique human-readable report IDs (e.g. `CF-1001`, `CF-1002`).
- [x] **CF-7**: Persistent SQLite storage surviving page refresh and server restarts.
- [x] **CF-9**: Live status and detailed view (`Submitted`, `In Progress`, `Resolved`) with case-insensitive ID lookup (**CF-19**).
- [x] **CF-13**: Staff status transition capability (`Submitted` ➔ `In Progress` ➔ `Resolved`).

### Sprint 2: Respond to Customer Feedback (Priority Change)
*Customer feedback: "Students sometimes submit a problem that already exists. Let them search existing reports by keyword or location before creating a new report."*
- [x] **CF-11**: Case-insensitive keyword search in both `title` and `description` with SQL wildcard escaping (**CF-20**).
- [x] **CF-12**: Location dropdown filtering and combined logical **AND** filter behavior with clean zero-match handling.
- [x] **CF-14**: Mandatory resolution note enforcement when transitioning a report to `Resolved`.
- [x] **CF-15**: Backend role enforcement and password-protected staff switching (**CF-21**), rejecting non-staff status updates with `403 Forbidden`.
- [x] **CF-17**: Staff-only restriction on `/api/reset-demo` (**CF-22**), preventing students from erasing demo data (`403 Forbidden`).

---

## Project Structure

```
campusfix/
├── app.py                              # Flask backend with REST endpoints & role-based session logic
├── database.py                         # SQLite persistence helper, queries, search AND logic, seeding
├── seed_data.py                        # Initial NTPU campus seed reports
├── .gitignore                          # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css                   # NTPU visual identity: deep blue #003366, gold, cards, responsive
│   └── js/
│       └── app.js                      # Client logic: validation, AJAX search, modals, role toggling
├── templates/
│   └── index.html                      # Clean NTPU-themed single page application
├── tests/
│   ├── test_campusfix.py               # Automated unittest suite covering TC-01 to TC-11
│   ├── test_A_title_length.py          # Part A: Title length limit tests (CF-18)
│   ├── test_B_report_id_case.py        # Part B: Case-insensitive report ID lookup tests (CF-19)
│   ├── test_C_search_escape.py         # Part C: SQL LIKE wildcard escaping tests (CF-20)
│   ├── test_D_staff_password.py        # Part D: Staff password authentication tests (CF-21)
│   └── test_E_reset_guard.py           # Part E: Demo reset staff guard tests (CF-22)
└── docs/
    ├── DATABASE_ERD.md                 # Database Entity-Relationship Diagram & schema specs
    └── reflections/                    # Individual team member reflections
```

---

## AI Usage Statement

Generative AI tools (Claude, Gemini / Antigravity, ChatGPT) were used during this project to assist with initial application scaffolding, defect analysis, unit test drafting, code review preparation, and documentation formatting. All generated code, defect fixes (Parts A–E), automated tests, and documentation were reviewed, executed, and verified by the respective team members on our local environments. Changes were reviewed through pull requests; #5 and #10 were reviewed after merging.
