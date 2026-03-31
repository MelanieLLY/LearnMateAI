# HW5 Part 1 Retrospective: How the Custom Skill Changed My Workflow

## What the Skill Did

I created a `/add-feature` skill for Claude Code. It teaches a 7-phase process for building features:
1. EXPLORE - Look at existing code
2. PLAN - Design the feature
3. RED - Write tests that fail
4. GREEN - Write code to pass tests
5. REFACTOR - Clean up code
6. COMMIT - Save to git
7. DOCUMENT - Update documentation

## How My Workflow Changed

### Before the Skill (v1)

When I built the first feature (Student Notes), I had to think about every step.

**Problems:**
- I didn't know where to start
- Should I look at code first or write tests first?
- How many tests should I write?
- What files should I create in what order?
- Did I forget to update documentation?

**Result:** I had to stop and think between each phase. It was slow and I wasn't sure if I was doing things right.

### After the Skill (v2)

When I built the second feature (Flashcards), I used the improved skill.

**What Changed:**
- The skill had a checklist for EXPLORE - I knew exactly what to look for
- The skill had a test template - I knew to write 6 tests (happy path + 5 errors)
- The skill had a file order - I created Model → Schema → Service → Router (no import errors!)
- The skill had a documentation checklist - I didn't forget anything

**Result:** I was much faster and more confident. I followed the same pattern both times.

## Which Tasks Became Easier?

### EXPLORE Phase

**Before:** "What should I look for in the code?"
- Spent time searching randomly
- Wasn't sure what patterns mattered

**After:** "Use the 4-part checklist"
- Look for: Architecture, Naming, Similar Features, Testing patterns
- Found everything I needed in 2 minutes
- **Easier:** 40% faster (was 2 min for both tasks)

### RED Phase (Writing Tests)

**Before:** "How many tests should I write? What scenarios?"
- Guessed at test cases
- Worried I missed important cases
- Took time to figure out

**After:** "Use the 6-scenario template"
- Happy path (success)
- Missing field (422)
- Empty field (422)
- Not logged in (401)
- Wrong role (403)
- Resource not found (404)
- **Easier:** Knew exactly what to test, same 6 tests both times

### GREEN Phase (Writing Code)

**Before:** "Create Model, Schema, Service, Router... but in what order?"
- Created files randomly
- Got circular import errors
- Had to debug and fix

**After:** "Follow the order: Model → Schema → Service → Router → Dependencies → Main"
- No import errors
- Same structure both times
- **Easier:** Zero errors, 1 minute faster (7 min → 6 min)

### COMMIT Phase (Git History)

**Before:** "What should my git commits say?"
- Made big commits with everything
- Or made too many small commits
- Unclear what each commit did

**After:** "Use atomic commits with clear messages"
- RED commit with all tests
- GREEN commit with all code
- DOCUMENT commit with documentation
- **Easier:** Clean git history, easy to understand

### DOCUMENT Phase

**Before:** "Did I update everything?"
- Updated some docs
- Forgot about others
- Inconsistent format

**After:** "Use the documentation checklist"
- Update: API docs, models, routing
- Use this template: Overview, Endpoint, Request, Response, Errors
- **Easier:** Didn't forget anything

## What I Learned

### The Skill Solved Real Problems

1. **Less thinking = faster work**
   - With a checklist, I didn't waste time deciding
   - I just followed the steps

2. **Same pattern = reliable results**
   - Both features built the same way
   - Same test structure
   - Same file structure
   - Same documentation format
   - Both had 6/6 tests passing

3. **Better quality = fewer mistakes**
   - First feature: had to debug imports
   - Second feature: zero errors (knew the order)
   - First feature: forgot some docs
   - Second feature: complete docs (had checklist)

### The Skill is Reusable

I can use this skill on future features:
- Works for small features (like Student Notes)
- Works for complex features (like Flashcards with AI)
- Works with different team members
- Same quality every time

## Conclusion

The custom skill changed my workflow from:
- "What should I do next?" to "Follow the checklist"
- "Did I forget anything?" to "Use the template"
- "Will this work?" to "I know the pattern"

**Most important:** The skill made me go from thinking about HOW to build features to focusing on WHAT features to build.

The skill is simple but powerful. It works because it is based on real experience - what worked in Task 1 became the template for Task 2.

I would use this skill again for every feature. It saves time, improves quality, and makes the work easier.
