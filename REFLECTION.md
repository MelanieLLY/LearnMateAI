# HW4 Reflection: Claude Code Workflow

## Part 1: Explore-Plan-Implement-Commit Workflow

### How Claude Code is Different

Previously we worked like this:
- Plan in Claude Web 
- Hand off concise prompts to Antigravity
- Review output quality before committing
- Work separately on different tasks
- Then start coding

Now with Claude Code:
- **EXPLORE** - Read existing code in terminal
- **PLAN** - Write down what we'll do
- **IMPLEMENT** - Write tests first, then code
- **COMMIT** - Save with clear messages

### Why This is Better

**No context switching:** Everything happens in Claude Code terminal.

**Real-time feedback:** We see code as we build it.

**Better coordination:** We work in same Claude Code session together.

**Faster:** Old workflow took longer per feature. New workflow is faster.

---

## Part 2: The 4 Steps

### STEP 1: EXPLORE

Read existing code to understand patterns:
- Find existing code files
- Find where similar code exists
- Learn how things are structured

Result: We know what exists before building.

---

### STEP 2: PLAN

Write down the approach:

**What we'll build:**
- Clear goal for the feature
- What needs to be done
- Write tests before code

**Reuse existing:**
- Check what already exists
- Follow existing patterns
- Use same code style

**Potential issues:**
- Think about what could go wrong
- Plan how to handle problems

Result: Clear plan before we code.

---

### STEP 3: IMPLEMENT (Red-Green-Refactor)

**RED: Write test that fails**

We write a test. The test fails because the code doesn't exist yet.

Result: Test fails (expected)

**GREEN: Write minimum code**

We write code to make the test pass. The test passes.

Result: Test passes

**REFACTOR: Make it better**

We improve the code while keeping tests passing.

Result: Test passes (better code)

**Result:** Tests prove code works.

---

### STEP 4: COMMIT

Save work with clear messages showing what was done.

Result: Git history shows the workflow.

---

## Part 3: Context Management Strategies

### Strategy 1: CLAUDE.md File

One file that explains the entire project:
- Tech Stack
- File Structure
- How we build
- Rules to follow

Why it works: New sessions read CLAUDE.md automatically. Time saved.

---

### Strategy 2: Use /compact and /clear

After working for a while, sessions can get slow.

**Solution:**
- Use /compact: Keep important info, remove old messages
- Use /clear: Fresh start for next feature

Why it works: Keeps sessions fast and focused.

---

### Strategy 3: Real-Time Teamwork

We both work in same Claude Code session:
- One person writes
- Other person reviews
- Switch roles as needed
- Decide together in real-time

Result: Better decisions, fewer mistakes.

---

## Part 4: How We Used This Workflow

### We built APIs using Claude Code following Explore-Plan-Implement-Commit

**What happened:**

We gave Claude descriptions of what tests should do.

Claude wrote the tests.

Tests failed (expected - no code yet).

Claude wrote minimum code to make tests pass.

Tests passed.

Claude improved the code quality.

Tests still passed.

We committed the work.

**We did this for multiple APIs:**

Each API followed the same pattern.

Each API had tests before code.

Each API was refactored for quality.

Each API has clear commit history.

**Session documentation includes:**

What we asked Claude to do
What Claude did
Whether tests failed or passed
Clear step-by-step progression

---

## Summary

### The Workflow is Faster

Old way was slower per feature.
New way is faster per feature.
We saved time overall.

---

### Why It Works

1. **Explore first** - We don't build same thing twice
2. **Plan before code** - No confusion during coding
3. **Tests first** - Code works or we see it fail
4. **Clean commits** - Git history tells the story
5. **Real-time teamwork** - We work together

---

### Key Learning

Claude Code is the opposite of our old workflow:
- Old: Plan in chat, hand off to tool, review, coordinate, code
- New: Explore, Plan, Implement, Commit (all in one place)

Result: Faster, clearer, better teamwork.
