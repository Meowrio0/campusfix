
# Individual Reflection – LI (Chu), Product Owner / Developer

My main responsibilities in the CampusFix project were serving as the Product Owner and developing Part C. As the Product Owner, I managed and prioritized Jira backlog items, including CF-11, CF-12, and CF-20. For Part C, I worked on keyword search, location filtering, and SQL wildcard escaping to improve the accuracy of search results.

Through this process, I became more familiar with version control and code review procedures.

Another responsibility was testing TC-06 to TC-08, which cover case-insensitive keyword search, location filtering, and searches with no matching results. I learned how to run tests using the terminal and how to connect test evidence with Jira issues.

One difficulty I faced was that I was initially unfamiliar with GitHub and terminal commands. Sometimes I did not know how to open the terminal, run tests, or understand the results. By practicing step by step, I gradually improved my ability to solve these problems.

Overall, this project taught me that software development involves more than writing code. Effective communication, teamwork, testing, and task management are equally important. In future projects, I hope to improve my technical skills and become more efficient in Agile team collaboration.

I used AI assistance to understand GitHub operations, troubleshoot issues, and improve the wording of this reflection. I reviewed the content and participated in the development and review process myself.

In addition, I participated in PR #2 to fix Issue C, where searching for `%` or `_` incorrectly returned all reports because these characters were treated as SQL wildcards.

I also worked with the related test cases to verify that special characters were handled correctly.

During the code review, an indentation error was identified in `database.py`, which helped me realize the importance of careful code review and testing.

In the future, I will run tests before submitting pull requests, check code changes more carefully, and provide clearer test evidence.

I will also improve communication by linking Jira issues, GitHub pull requests, and test results to make the development process more organized and traceable.

