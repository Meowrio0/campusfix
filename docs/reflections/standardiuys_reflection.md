# Individual Reflection — 王柏森 (standardiuys), Scrum Master

My technical contribution was Part B (Jira story CF-6 and bug CF-19). CampusFix could find `CF-1001`, but it treated `cf-1001` as a numeric primary key and returned HTTP 404. In branch `fix/B-id-case` and [PR #3](https://github.com/Meowrio0/campusfix/pull/3), I updated `get_report_by_id()` and `update_report_status()` in `database.py` to convert the input to uppercase before checking the prefix. This also makes sure the SQL query receives the uppercase ID.

My main difficulty was writing a test that showed the fix worked. My first test file copied the existing suite, and a teammate pointed that out during review. I rewrote `tests/test_B_report_id_case.py` with two focused tests. The first checks that `CF-1001` and `cf-1001` both return HTTP 200 and the same report. The second checks that staff can update the report status using a lowercase ID and that the change is saved in the database. The reviewer reported that all 13 automated tests passed in GitHub Codespaces.

As Scrum Master, I spent too much time on my own fix and could have checked in with teammates sooner. I should have asked who was stuck and which pull requests were still waiting for a reviewer.I'm still not entirely clear on how to run a team project. I did very little to coordinate the team or follow up on everyone’s progress. Next time, I should set up a clear workflow from the start and bring everyone together to complete the project.

I used AI to help draft the test code and revise this reflection.
