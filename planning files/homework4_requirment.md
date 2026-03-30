> 🛑 **STATUS: SUBMITTED & DONE** 🛑
> Homework 4 has already been submitted on a separate branch. 
> All strict HW4 requirements (using Claude Code CLI, forced TDD commit history, etc.) can now be completely IGNORED. We are free to refactor and develop normally.

## HW4: Claude Code Workflow & TDD

**Due:** Sunday by 11:59pm | **Points:** 50 | Pair Work Encouraged

### Author
老师的官方要求

### Objective
Demonstrate mastery of the Claude Code development workflow by setting up a project, using the Explore→Plan→Implement→Commit pattern, and doing TDD through Claude Code.

### Part 1: Claude Code Project Setup (25%)
Set up Claude Code for your P3 project:
- Write a comprehensive `CLAUDE.md` (project context, stack, conventions, do's/don'ts).
- Configure permissions (allowlists or sandboxing).
- Demonstrate `/init` output and iterate on `CLAUDE.md` based on it.
- Show context management strategy (`/clear`, `/compact`, `--continue`).

**Requirements:** `CLAUDE.md` must include: tech stack, architecture decisions, coding conventions, testing strategy, and project-specific do's/don'ts. At least one `@import` reference to additional context (e.g., PRD, API docs).

### Part 2: Explore → Plan → Implement → Commit (30%)
Use Claude Code's recommended 4-phase workflow on a real P3 feature:
- **Explore:** Use Glob, Grep, Read to understand existing code.
- **Plan:** Use Plan mode to design the approach.
- **Implement:** Execute the plan with Claude Code.
- **Commit:** Create clean commits with meaningful messages.

**Requirements:** Git history must clearly show this workflow. At least 3 commits demonstrating the pattern.

### Part 3: TDD with Claude Code (30%)
Build a P3 feature using strict TDD through Claude Code:
- Write failing tests first (**Red**).
- Have Claude Code implement minimum code to pass (**Green**).
- Refactor as necessary (**Refactor**).
- Repeat for all acceptance criteria.

**Requirements:** Tests written BEFORE implementation. Git history shows red-green-refactor commits. Clear commit messages showing TDD process.

### Part 4: Reflection (15%)
Write a 1-2 page reflection answering:
- How does the Explore→Plan→Implement→Commit workflow compare to your previous approach?
- What context management strategies worked best?
- Include annotated Claude Code session log showing your workflow.

### Deliverables
- P3 repository with `CLAUDE.md` and permissions configuration.
- Feature code with TDD git history (red-green-refactor commits).
- Annotated Claude Code session log.
- Reflection document (1-2 pages).

### Rubric Overview
| Criterion | Weight | Points |
| :--- | :--- | :--- |
| CLAUDE.md & project setup | 25% | 12.5 |
| Explore→Plan→Implement→Commit workflow | 30% | 15 |
| TDD process through Claude Code | 30% | 15 |
| Reflection & session log | 15% | 7.5 |

### Detailed Scoring Rubric

| Criteria | Pts | Ratings & Descriptions |
| :--- | :--- | :--- |
| **CLAUDE.md & Project Setup** | 12.5 pts | **12.5 pts (Excellent):** Comprehensive and accurate.<br>**9.5 pts (Good):** Well-setup, most features present.<br>**6.25 pts (Adequate):** Acceptable, basics covered.<br>**3 pts (Needs Improvement):** Poor documentation.<br>**0 pts (No Marks):** Missing file or configuration. |
| **Explore→Plan→Implement→Commit Workflow** | 15 pts | **15 pts (Excellent):** Mastery shown through clear git history.<br>**11.25 pts (Good):** Workflow clearly followed with minor issues.<br>**7.5 pts (Adequate):** Workflow partially followed.<br>**3.75 pts (Needs Improvement):** Minimal evidence of workflow.<br>**0 pts (No Marks):** Workflow not followed. |
| **TDD Process through Claude Code** | 15 pts | **15 pts (Excellent):** True red-green-refactor commits for each feature.<br>**11.25 pts (Good):** TDD followed for most features.<br>**7.5 pts (Adequate):** TDD basics achieved.<br>**3.75 pts (Needs Improvement):** Inconsistent TDD process.<br>**0 pts (No Marks):** No TDD followed. |
| **Reflection & Session Log** | 7.5 pts | **7.5 pts (Excellent):** Deep reflection and well-annotated logs.<br>**5.625 pts (Good):** Good reflection and logs.<br>**3.75 pts (Adequate):** Basic reflection and logs.<br>**1.875 pts (Needs Improvement):** Poor reflection or incomplete logs.<br>**0 pts (No Marks):** Missing documentation. |
| **Total Points** | **50** | |