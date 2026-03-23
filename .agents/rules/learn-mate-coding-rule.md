---
trigger: always_on
description: Mandatory workflow for adding or modifying features (Issue creation, sprint plan update, branching)
---

# Feature Development Workflow (ALWAYS DO THIS)
Whenever the user asks to add a new feature or modify an existing feature, you MUST strictly follow these steps before starting codebase implementation:
1. **Issue Management**: Check GitHub Issues (via `gh` CLI). Create a new issue or update an existing one with clear descriptions. Always assign appropriate labels and a milestone.
2. **Sprint Plan Update**: Update `planning files/learnmate-sprint-plan.md` to map the new issue and feature. 
3. **Branching**: Checkout a new branch named appropriately according to the conventional standard with the issue ID (e.g., `feat/12-new-feature` or `fix/13-fix-bug`). YOU MUST ALWAYS branch out.
