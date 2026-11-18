# Individual Reflection – 林健勛 (Meowrio0), Developer

My technical contribution was Part A, the report title length limit (Jira story CF-5, bug CF-18). While testing the initial version, I found that a 5,000-character title could be submitted. I fixed it in branch `fix/A-title-length` and pull request #1. The Flask backend (`submit_report()` in `app.py`) now rejects titles longer than 100 characters with HTTP 400 and a field-specific message, the form shows the same error before sending, and the title input has a `maxlength`. I added `tests/test_A_title_length.py` with three tests: 101 characters rejected, exactly 100 accepted, and 5,000 rejected with nothing saved. The backend check matters most, because a request that bypasses the page must still be rejected.

I also helped organise the team. I created the team GitHub repository, invited the members, wrote the A–E work split with branch and pull-request rules, logged the five defects as Jira bugs (CF-18 to CF-22), and reviewed Axel's pull request #4 (CF-17), requesting a frontend message and a data-preservation test.

One difficulty was Git itself. My first commit used a placeholder e-mail, so it was not linked to my account. I learned to set `user.email` correctly, amend the commit, and force-push only my own branch with `--force-with-lease`.

One improvement for next time is to write the test for a defect first, then fix it, so the test proves the bug and the fix.

I used AI assistance to draft and review the code and this reflection. I reviewed and tested the changes myself and can explain them.
