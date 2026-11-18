# Test evidence – Louis Imbert (Louis-ibt)

**Tester:** Louis Imbert · **Date:** 2026-11-18 · **Code tested:** `main` at `25f7f72` (A, D and E merged)
**Environment:** Windows 11, Python 3.13, Flask 3.1.3, Chromium (Playwright), app started with `python app.py`
and `CAMPUSFIX_STAFF_PASSWORD` set.

Each case was run twice: manually in the running app (screenshots below) and with the automated test.
Automated output: [`TC-04-TC-10-automated.txt`](TC-04-TC-10-automated.txt) (9 passed; full suite 27 passed).

---

## TC-04 – Persistence after refresh and restart (Jira CF-7)

**Objective:** a submitted report is still stored after a page refresh and after the server is stopped and restarted.

| Step | Action | Result | Evidence |
| :-- | :-- | :-- | :-- |
| 1 | As student, submit "TC-04 Persistent projector issue (Louis)", College of Social Sciences, Classroom Equipment | Report **CF-1006** created, status `Submitted`, 2026-11-18 21:32:01 | [TC-04-1](TC-04-1-report-submitted.png) |
| 2 | Refresh the page | CF-1006 still listed with the same data | [TC-04-2](TC-04-2-after-refresh.png) |
| 3 | Stop the Flask server (port 5000 no longer listening), start it again (new process) and reload | CF-1006 still there: same title, description, status and timestamps | [TC-04-3](TC-04-3-after-server-restart.png) |

**Expected:** the report survives refresh and restart unchanged. **Actual:** as expected. **Outcome: PASS**
Automated: `test_04_persistence_after_restart` PASSED.

---

## TC-10 – Student prevented from staff update actions

**Objective:** a student cannot change a report status, neither from the interface nor by calling the API directly.

| Step | Action | Result | Evidence |
| :-- | :-- | :-- | :-- |
| 1 | As student, look at CF-1006 in the list | Only "View Details" is offered, no status action | – |
| 2 | Force the status dialog (`openStatusModal('CF-1006')`) | Blocked: "Access Denied: Only staff members are permitted to update report status." | [TC-10-1](TC-10-1-student-ui-blocked.png) |
| 3 | As student, send `POST /api/reports/CF-1006/status` with `status: Resolved` directly (bypassing the page) | **HTTP 403**, `Access denied: Only university staff members...` | [TC-10-2](TC-10-2-api-student-403.txt) |
| 4 | Read CF-1006 again | Still `Submitted`, `updated_at` unchanged | [TC-10-2](TC-10-2-api-student-403.txt) |

**Expected:** 403 and data unchanged. **Actual:** as expected. **Outcome: PASS**
Automated: `test_10_student_prevented_from_staff_update_actions` PASSED.

---

## Retest of bug CF-21 (Part D, fixed in PR #5)

| Step | Action | Result | Evidence |
| :-- | :-- | :-- | :-- |
| 1 | As student, click "Switch to Staff" and enter a wrong password | "Incorrect staff password.", role stays **Student** | [D-1](D-1-wrong-password-refused.png) |
| 2 | Click "Switch to Staff" and enter the correct password | "Switched active account to: Staff Demo", role **Staff** | [D-2](D-2-correct-password-staff.png) |
| 3 | Switch back to student | No password asked, role Student | – |

**Outcome: PASS** · Automated: `tests/test_D_staff_password.py` 7/7 PASSED.

Note: in the screenshots, the password was entered by script (replacing the browser prompt), so that the
6-second confirmation message could be captured; the request sent to the server is the same as a manual entry.
