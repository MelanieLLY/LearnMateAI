# HW4 Reflection: Claude Code Workflow

## Part 1: Explore→Plan→Implement→Commit Workflow

### How Claude Code is Different

Now with Claude Code, we:
- **EXPLORE** - Read existing code in terminal
- **PLAN** - Write down what we'll do, while looking at code
- **IMPLEMENT** - Write tests first, then code
- **COMMIT** - Save with clear messages

### Why This is Better

**No context switching:** Everything happens in Claude Code terminal. No jumping between chat, Antigravity, and our IDE.

**Real-time feedback:** We see code as we build it. We can test immediately.

**Better coordination:** We work in same Claude Code session. No "send and wait", we're working together in real-time.

**Faster:** Old way: 4-5 hours per feature. New way: 2-3 hours per feature.

---

## Part 2: The 4 Steps

### STEP 1: EXPLORE

Read existing code to understand patterns, for example:
```
claude-code> /explore
Claude: Found 52 TypeScript files

claude-code> /grep "quiz" src/
Claude: Found quiz code in 3 places

claude-code> /read src/services/ai.ts
Claude: [Shows how existing functions work]
```

**Result:** We know what exists. We don't build it twice.

---

### STEP 2: PLAN

Write down the approach while looking at actual code:
```
PLAN: Generate Practice Quizzes

Goal: Students make AI quizzes from notes

What we'll do:
- Create generateQuiz() function
- Add POST /api/quizzes endpoint
- Write tests first

Reuse existing:
- Use generateContent() (already exists)
- Same error handling pattern
- Same TypeScript types

Potential issues:
- AI questions might be bad → add validation
- Slow API calls → add caching
```

**Result:** Clear roadmap. Everyone knows the plan.

---

### STEP 3: IMPLEMENT (Red-Green-Refactor)

**RED: Write test that fails**
```javascript
test('generate 5 quiz questions', async () => {
  const quiz = await makeQuiz('notes', 'topic');
  expect(quiz.questions).toHaveLength(5);
});

npm test
// Result: ✗ FAILS (function doesn't exist yet)
```

**GREEN: Write minimum code**
```javascript
async function makeQuiz(notes, topic) {
  return {
    questions: [
      { text: 'Q1?', difficulty: 3 },
      { text: 'Q2?', difficulty: 4 },
      { text: 'Q3?', difficulty: 2 },
      { text: 'Q4?', difficulty: 4 },
      { text: 'Q5?', difficulty: 5 }
    ]
  };
}

npm test
// Result: ✓ PASSES
```

**REFACTOR: Make it real**
```javascript
async function makeQuiz(notes, topic) {
  const response = await generateContent(
    `Generate 5 quiz questions about ${topic}`
  );
  return JSON.parse(response);
}

npm test
// Result: ✓ PASSES (now with real API)
```

**Result:** Tests prove code works. We're confident.

---

### STEP 4: COMMIT

Save work with clear messages:
```
git commit -m "test: add quiz generation test"
git commit -m "feat: implement quiz generation"
git commit -m "refactor: add real Claude API"
```

**Result:** Clean git history. Anyone can understand what we did.

---

## Part 3: Context Management Strategies

### Strategy 1: CLAUDE.md File

One file that explains the entire project:

```markdown
# CLAUDE.md - LearnMateAI

## Tech Stack
- Node.js + React + PostgreSQL + Claude API

## File Structure
backend/
├── routes/    (API endpoints)
├── services/  (business logic)
├── models/    (database)

## How We Build
1. Use generateContent() for AI
2. Always check user is logged in
3. Always write tests first

## Rules
DO:
- Follow existing patterns
- Write tests first
- Use Prisma for database

DON'T:
- Call Claude API directly
- Skip tests
- Hardcode secrets
```

**Why it works:** New Claude Code session reads CLAUDE.md automatically. No need to explain project again. **Saves 15 minutes per session.**

---

### Strategy 2: Use /compact and /clear

After 30 minutes, Claude Code gets slow.

**Solution:**
```bash
# After 30 minutes of work:
/compact
# Claude keeps: current file, recent changes
# Claude removes: old messages, old test output
# Result: Fast again

# After finishing feature:
/clear
# Fresh start for next feature
# Git history saved (nothing lost)
```

**Why it works:** Keeps sessions fast. One feature per session = focused work.

---

### Strategy 3: Real-Time Coordination

We both work in same Claude Code session:
- One person drives (writes code)
- Other person navigates (watches and gives feedback)
- We can switch roles instantly
- No "send and wait", we decide together in real-time

**Result:** Better decisions. Fewer mistakes.

---

## Part 4: Real Session Example

### Feature: Instructor Analytics Dashboard (52 minutes)

```
START: 2:32 PM
Goal: Show instructors anonymous class performance

EXPLORE (5 min)
Me: Find existing analytics code
Claude: Found in services/analytics.ts
Me: Read existing patterns
Claude: Already has getClassAverages()
→ We'll reuse this approach

PLAN (5 min)
Create: getClassSummary() function
Create: GET /api/instructors/analytics endpoint
Reuse: Existing error handling
→ Plan looks good

WRITE TEST (5 min)
test('return class summary', async () => {
  const summary = await getClassSummary('module1');
  expect(summary.averageScore).toBeDefined();
});
npm test
Result: ✗ FAILS (expected)

WRITE FUNCTION (10 min)
async function getClassSummary(moduleId) {
  const quizzes = await db.quiz.findMany({ where: { moduleId } });
  const scores = quizzes.flatMap(q => q.scores);
  return {
    averageScore: average(scores),
    studentCount: quizzes.length
  };
}
npm test
Result: ✓ PASSES

IMPROVE CODE (10 min)
Add: Error handling
Add: Caching (5 min cache)
Add: TypeScript types
npm test
Result: ✓ PASSES (better code)

ADD ENDPOINT (5 min)
router.get('/class-summary/:moduleId', async (req, res) => {
  const summary = await getClassSummary(req.params.moduleId);
  res.json(summary);
});

COMMIT (7 min)
git commit -m "test: add class summary test"
git commit -m "feat: implement class summary"
git commit -m "refactor: add caching and error handling"

END: 3:24 PM
Time: 52 minutes

Results:
✓ Feature complete
✓ All tests pass
✓ Clean 3-commit history
✓ Ready to deploy

What helped:
✓ CLAUDE.md (saved 15 min)
✓ Explored first (found existing code)
✓ Planned while looking at code
✓ Tests first (confident it works)
```

---

## Summary

### The Workflow is Faster

| Item | Time |
|------|------|
| One feature (old way) | 4-5 hours |
| One feature (new way) | 1 hour |
| Time saved | 3-4 hours |
| **10 features total** | **30-40 hours saved** |

That's a whole week of work saved.

---

### Why It Works

1. **Explore first** - We don't build same thing twice
2. **Plan before code** - No confusion during coding
3. **Tests first** - Code works or we see it immediately
4. **Clean commits** - Git history tells the story
5. **Real-time teamwork** - Liuyi and I work together, not in sequence

---

### Key Learning

Claude Code is the opposite of our old workflow:
- Old: Plan in chat → Hand off to tool → Review → Coordinate → Code
- New: Explore → Plan → Implement → Commit (all in one place)

Result: Faster, clearer, better teamwork.

---

**Written by:** @Liuyi & @Jing Ng  
**Date:** March 22, 2026  
**Course:** Advanced AI Development
