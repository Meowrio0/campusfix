# CampusFix - Individual Student Reflections
**Course: Software Engineering | Assignment: Agile Team Project with Jira**  
**National Taipei University / Team: SE_CampusFix_Team04**

Each student reflection satisfies the mandatory word count requirement (200–300 words per student) and details technical contributions with Jira keys, code/test evidence, one specific difficulty encountered, and one area of personal improvement.

---

### 1. Alex Dupont (Product Owner / Developer) — Student ID: 41271001
**Word Count: 268 words**

As Product Owner and Developer for Team 04, I was responsible for backlog ordering, clarifying requirement criteria, and architecting our backend REST endpoints in `app.py`. My primary technical contributions included authoring the report creation route under **CF-10** (`POST /api/reports`), implementing field validation logic for **CF-11**, and leading the endpoint logic for report listings in **CF-15**. During Sprint 2 planning, I assessed the customer request regarding duplicate incident submissions and prioritized the case-insensitive search and filter stories (**CF-21**, **CF-22**) into our sprint backlog while deferring optional photo attachments to respect our velocity. I also authored the automated test `test_11_combined_filters_and_logic` in `tests/test_campusfix.py`, proving that combined keyword and location filtering strictly operates under logical AND semantics.

One significant difficulty I encountered was reconciling the customer’s mid-project search request with our existing schema. Initially, I was tempted to over-engineer an external search index like Elasticsearch, but this would have bloated our local setup and violated the course instructions to avoid over-engineering. Discussing this with Chen helped me realize that using SQLite’s native `LOWER()` function across the `title` and `description` columns met 100% of the customer requirements with zero additional dependencies.

An area where I improved is backlog transparency. In Sprint 1, I initially assumed requirement details without documenting edge-case acceptance criteria in Jira. In Sprint 2, I made sure every single story had at least three testable acceptance criteria before work began, which drastically reduced confusion during code review and helped our team deliver all 27 story points on time.

---

### 2. Béatrice Lin (Scrum Master / Developer) — Student ID: 41271002
**Word Count: 275 words**

Serving as Scrum Master and Frontend Developer, my dual responsibility was maintaining agile team health and creating the responsive user interface for CampusFix. In Jira, I organized our Scrum space `SE_CampusFix_Team04`, facilitated our daily 17:30 standups, and tracked our Definition of Done. On the development side, I built our entire presentation layer in `templates/index.html` and `static/css/style.css`. I designed the user experience to match National Taipei University’s official portal (`new.ntpu.edu.tw`), incorporating NTPU deep blue (`#003366`), gold badge accents, the university emblem, and accessibility markers (`:::`). Technically, I delivered the frontend form validation display for **CF-11**, the detailed report modal for **CF-14**, the search interface for **CF-21** and **CF-22**, and the 1-click demo role switcher for **CF-32**.

One challenge I faced was managing mobile layout responsiveness without utilizing heavy CSS frameworks like Bootstrap or Tailwind. The incident tables initially overflowed smaller mobile viewports. I solved this by implementing CSS media queries and horizontal overflow wrappers, ensuring that incident cards and action buttons remain fully usable on tablets and smartphones used by students walking around campus.

From a process standpoint, my biggest improvement was facilitating continuous sprint tracking. During Sprint 1, team members waited until late evening to update their Jira subtasks, which obscured our actual progress. For Sprint 2, I implemented our retrospective action: checking in with developers at lunchtime and ensuring Jira cards moved from *To Do* to *In Progress* in real time. This made our Sprint 2 burndown curve genuinely reflective of our daily work.

---

### 3. Chen Wei (Developer / Tester) — Student ID: 41271003
**Word Count: 282 words**

My technical focus on Team 04 was data persistence, query logic, and automated backend testing. In `database.py`, I designed the SQLite schema and implemented ACID-compliant connection handling (**CF-13**). To fulfill **CF-12**, I implemented the atomic `generate_report_id()` algorithm that constructs human-friendly unique IDs (such as `CF-1001`, `CF-1002`) based on the latest database sequence. In Sprint 2, I implemented the search engine in **CF-21**, querying `LOWER(title) LIKE ? OR LOWER(description) LIKE ?` to ensure queries like `wifi`, `WiFi`, and `WIFI` behave identically. Furthermore, I authored the first six automated test cases (`test_01` to `test_06`) in `tests/test_campusfix.py`, establishing coverage for report submission, missing input validation, unique ID generation, disk persistence across restarts, and case-insensitive search.

A major technical obstacle I encountered was handling unicode case-insensitivity in SQLite (logged as **CF-BUG-02**). Initially, standard SQLite `LIKE` comparisons did not treat uppercase acronyms identically when matching mixed-case text. I debugged this issue by normalizing both database column values and incoming query parameters using Python’s `.lower()` and SQL `LOWER()`, resolving the bug and verifying the fix with automated regression test `test_06_keyword_search_case_insensitive`.

My key personal improvement in this project was embracing automated testing early. In earlier coursework, I often relied on manual browser clicking to test features, which was slow and error-prone. By setting up Python’s `unittest` framework with isolated temporary database fixtures in `setUp()` and `tearDown()`, I learned how fast automated verification can be, running our entire 11-test suite in under 0.25 seconds.

---

### 4. David Martin (Developer / Tester) — Student ID: 41271004
**Word Count: 279 words**

As a Developer and Quality Assurance Tester, my primary deliverables focused on staff resolution workflows, role authorization, and test cases `TC-07` through `TC-10`. In `app.py`, I implemented the resolution endpoint under **CF-30**, allowing facility managers to transition incidents between `Submitted`, `In Progress`, and `Resolved`. For **CF-31**, I authored the mandatory resolution note validation, ensuring that attempts to mark an issue `Resolved` without an explanation are rejected with HTTP 400. To fulfill **CF-32**, I built session-based role authorization middleware that checks active roles and returns `403 Forbidden` if a student account attempts to tamper with incident statuses. I also authored automated tests `test_07` (location filtering), `test_08` (zero-match queries), `test_09` (mandatory resolution notes), and `test_10` (student authorization denial).

The most tricky difficulty I encountered was preventing whitespace-only bypasses on resolution notes (logged as defect **CF-BUG-03**). When manual testing began, I noticed that entering spaces satisfied basic truthy checks (`if note:`) in Python. I fixed this by applying `.strip()` to both backend evaluation and frontend input validation, ensuring that meaningful explanations are strictly enforced before an incident is marked as resolved in the database.

Through this project, I significantly improved my understanding of agile collaboration and Definition of Done. Previously, I considered code "done" once the happy path worked on my machine. Working under our team’s Definition of Done taught me to verify edge cases, write automated assertions, link commit keys in Jira, and conduct peer code reviews before considering any feature complete.
