# CampusFix - National Taipei University (NTPU) Problem Resolution System
**Software Engineering Course | Team Project | SE_CampusFix_Team04**

CampusFix is a lightweight campus incident and facility problem reporting web application built for National Taipei University. It empowers students to report physical campus defects (classroom projectors, Wi-Fi outages, plumbing leaks, etc.), tracks live resolution progress, enables case-insensitive search and filtering to avoid duplicate submissions, and provides a staff workflow with mandatory resolution notes.

The user interface follows the official visual identity of the [NTPU Portal](https://new.ntpu.edu.tw/), utilizing Taipei Tech/NTPU deep blue (`#003366`), gold accents (`#C5A059`), card containers, accessibility markers (`::: Skip to main content`), and clean responsive tables.

---

## Team Members & Roles (Team 04)

| Name | Role | Student ID | Primary Responsibilities |
| :--- | :--- | :--- | :--- |
| **Alex Dupont** | Product Owner / Developer | 41271001 | Backlog ordering, Scope decisions, Flask API routing, Sprint planning |
| **Béatrice Lin** | Scrum Master / Developer | 41271002 | Scrum ceremony facilitation, Jira board management, Frontend UI/UX, NTPU theme |
| **Chen Wei** | Developer / Tester | 41271003 | SQLite database persistence, Case-insensitive search, Test suite (TC-01 ~ TC-06) |
| **David Martin** | Developer / Tester | 41271004 | Staff authorization & resolution workflow, Validation rules, Test suite (TC-07 ~ TC-11) |

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
```bash
python app.py
```
Open your web browser and navigate to:
👉 **`http://127.0.0.1:5000`**

The database (`campusfix.db`) initializes automatically with realistic NTPU campus reports.

### 3. Run Automated Tests
Execute the comprehensive test suite covering all 10 required test cases + edge cases:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
Output:
```text
...........
----------------------------------------------------------------------
Ran 11 tests in 0.208s

OK
```

---

## Demonstration Accounts

As specified in the assignment handout, predefined demonstration accounts are provided. You can switch between roles in **1 click** using the top-right role switcher on the navigation bar:

1. **Student Account (`student@ntpu.edu.tw`)**:
   - Role: `student`
   - Permissions: Can submit new problem reports, search existing reports, view report details.
   - Restricted: Cannot modify report status or write resolution notes (server returns `403 Forbidden` if attempted).

2. **Staff Account (`staff@ntpu.edu.tw`)**:
   - Role: `staff` (Office of General Affairs / Facility Division)
   - Permissions: Can review all incoming reports, change status (`Submitted` ➔ `In Progress` ➔ `Resolved`), and provide mandatory resolution notes upon closing an issue.

---

## Features Delivered Across Sprints

### Sprint 1: Deliver Basic Workflow
- [x] **CF-10**: Problem report submission form (Title, Location, Category, Description).
- [x] **CF-11**: Strict field validation with individual error messages for missing/whitespace inputs.
- [x] **CF-12**: Automated generation of unique human-readable report IDs (e.g. `CF-1001`, `CF-1002`).
- [x] **CF-13**: Persistent SQLite storage surviving page refresh and server restarts.
- [x] **CF-14**: Live status and detailed view (`Submitted`, `In Progress`, `Resolved`).
- [x] **CF-30**: Initial staff status transition capability.

### Sprint 2: Respond to Customer Feedback (Priority Change)
*Customer feedback: "Students sometimes submit a problem that already exists. Let them search existing reports by keyword or location before creating a new report."*
- [x] **CF-21**: Case-insensitive keyword search in both `title` and `description`.
- [x] **CF-22**: Location dropdown filtering across campus buildings.
- [x] **CF-23**: Clean handling of zero-match search results with user guidance.
- [x] **CF-24**: Combined filter logical **AND** behavior (keyword matches title/description AND location matches selection).
- [x] **CF-31**: Mandatory resolution note enforcement when transitioning a report to `Resolved`.
- [x] **CF-32**: Backend role enforcement rejecting non-staff status updates with `403 Forbidden`.

---

## Project Structure

```
campusfix/
├── app.py                     # Flask backend with REST endpoints & role-based session logic
├── database.py                # SQLite persistence helper, queries, search AND logic, seeding
├── campusfix.db               # SQLite database file (created on initial launch)
├── .gitignore                 # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css          # NTPU visual identity: deep blue #003366, gold, cards, responsive
│   └── js/
│       └── app.js             # Client logic: validation, AJAX search, modals, role toggling
├── templates/
│   └── index.html             # Clean NTPU-themed single page application
├── tests/
│   ├── __init__.py
│   └── test_campusfix.py      # Automated unittest suite covering 11 test scenarios
└── docs/
    ├── README.md              # Project documentation
    ├── PROJECT_IMPLEMENTATION_GUIDE_A_TO_Z.md # End-to-end implementation roadmap & realistic time breakdown
    ├── DATABASE_ERD.md        # Database Entity-Relationship Diagram (Mermaid) & schema specs
    ├── TEAM_REPORT.md         # Formal 5-page Team Report (Agile process, Sprints, Retrospectives)
    ├── JIRA_BACKLOG_GUIDE.md  # Jira Scrum guide: Epics, 10 Stories, Dailies, Bugs, DoD
    ├── TEST_RECORD.md         # Formal Test Record with 10 required cases + Bug reproduction logs
    ├── INDIVIDUAL_REFLECTIONS.md # 4 individual student reflection essays (200-300 words each)
    └── DEMO_SCRIPT.md         # 7-minute demonstration oral presentation guide
```
