# HW4 Reflection: Claude Code Workflow & TDD

**Date:** March 22, 2026

## 1. Comparing the Explore→Plan→Implement→Commit Workflow to Previous Approaches

Before using Claude Code, my AI development workflow was pretty fragmented. I usually kept switching between my IDE and a browser-based AI interface. If I ran into an issue or needed to build something new, I had to type out the problem, copy-paste my code, wait for the AI to give me an answer, and then try to fit that code back into my project. This back-and-forth process often caused bugs because the AI didn't know how my whole project was connected. On top of that, testing was usually just an afterthought that I did at the very end.

The **Explore→Plan→Implement→Commit** workflow inside Claude Code changed how I work. Having the AI right inside my terminal meant it had direct access to the actual files in my codebase. When we worked on the **Instructor Module Management API (Create/Edit/Delete)**, the difference was obvious right away:

### The Explore Phase
Instead of me having to explain how our code is set up, Claude used terminal commands like `Glob` and `Grep` to look at our FastAPI routes, Pydantic models, and Pytest configuration before writing any code. This made sure the new API features actually fit into our existing project and reused things like our current authentication code, rather than making up a new structure from scratch.

### The Plan Phase
Instead of just asking the AI to "write the endpoint," we took a step back and made a plan. We wrote down exactly which edge cases we needed for the Create, Edit, and Delete routes. For example, we planned out the 200/201 success paths, the 422 errors for missing titles, the 409 errors for duplicate titles, and the 401/403 authorization checks. Planning this out beforehand saved us from the usual trial and error coding loops.

### Implementation Driven by Testing (TDD)
This was the biggest change for me. We followed a strict Test-Driven Development (Red-Green-Refactor) loop. Before writing any actual business logic, Claude wrote out the Pytest files based on our plan (the RED phase). We ended up writing 17 tests across the three modules. We ran them in the terminal to watch them fail, which proved that the tests were working correctly.

![RED Phase Failing Tests](/Users/melaniey/Github/LearnMateAI/docs/screenshot/01_RED_phase_failing_tests.png)
*Caption: The RED phase, demonstrating failing tests for the Create Module API before any routing logic was implemented.*

Only after confirming the failing tests did we write the minimum code needed to make them pass (the GREEN phase). Once Pytest showed a 100% pass rate, we went back to refactor the code (the REFACTOR phase) to make sure it followed PEP 8 style guidelines and had good docstrings. TDD basically forced us to prove our code worked instead of just running the server and hoping for the best.

### Step-by-Step Commits
Because we developed in small, verified steps, our Git history turned out really clean. We made simple, step-by-step commits (like `test(#2): RED - add failing tests for create module API`, followed by `feat(#2): GREEN...`). This left us with a git log that actually tells the story of how we built the feature, which is a lot better than the massive, messy "initial commit" dumps I used to do.

![Final TDD Commits History](/Users/melaniey/Github/LearnMateAI/docs/screenshot/08_Final_TDD_commits_history.png)
*Caption: A segment of our final Git log, clearly showing the Red-Green-Refactor commit history for the Instructor Module endpoints.*

Overall, this loop broke my habit of constant context-switching and made testing the main focus of the project.

---

## 2. Context Management Strategies That Worked Best

For this assignment, we had to implement three different APIs, and running Pytest created a lot of terminal output. When using an AI agent in the terminal, managing the context window is super important so the AI doesn't get confused or slow down. Two specific strategies really helped us here:

### Using `CLAUDE.md` as a Guide
Setting up a good `CLAUDE.md` file saved us a lot of time. By writing down our exact tech stack (Python 3.12, FastAPI, SQLAlchemy, Pytest) and our coding rules (PEP 8, docstrings), Claude knew exactly what to do from the start. When we ran `/init`, Claude even noticed some outdated Next.js and Prisma commands left over from an old setup and fixed them for us. Because this file was always loaded in the background, I never had to waste prompt tokens reminding the AI that we were building a FastAPI backend. 

### Clearing the Terminal with `/compact`
Since our TDD process involved running tests that threw long Python stack tracebacks when they failed, the working memory got full pretty fast. To keep the agent from getting slowed down by old error logs, the `/compact` command was a lifesaver.

We used `/compact` to throw away the long error logs while keeping a short summary of the progress we had made. This kept the agent focused. For example, when we finished the Create API and moved on to the Edit API, running `/compact` made sure Claude wasn't still thinking about the error messages from the previous API's RED phase. It gave us a clean slate for the next task without erasing the knowledge of what we just built.

## Conclusion

Moving away from manually copying and pasting code to using the Explore→Plan→Implement→Commit workflow has made my coding process a lot more organized. By sticking to TDD and using context management commands like `/compact` and a proper `CLAUDE.md` file, we were able to finish the Instructor Module Management API with a clean codebase and a Git history that I'm actually proud to turn in.
