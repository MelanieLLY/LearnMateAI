### Git Commit History 

All 3 agents follow RED-GREEN-REFACTOR TDD pattern:

**Agent 1 (Flashcard - Issue #3):**

<img width="665" height="50" alt="Screenshot 2026-04-12 at 8 39 05 PM" src="https://github.com/user-attachments/assets/90c75ece-d801-492f-adc8-49fd2cb72fce" />

**Agent 2 (Summary - Issue #4):**

<img width="570" height="42" alt="Screenshot 2026-04-12 at 8 38 16 PM" src="https://github.com/user-attachments/assets/c8818a30-5a34-45a3-90d7-20044bbc715d" />

**Agent 3 (Quiz - Issue #31):**

<img width="563" height="51" alt="Screenshot 2026-04-12 at 8 37 35 PM" src="https://github.com/user-attachments/assets/3d19146f-cd29-4fa2-92eb-16b27e511d10" />

Total: 9 commits showing TDD workflow

### GitHub Commit History 

All 9 commits are visible on GitHub main branch at:
https://github.com/MelanieLLY/LearnMateAI/commits/main

<img width="1109" height="468" alt="Screenshot 2026-04-12 at 8 41 29 PM" src="https://github.com/user-attachments/assets/3e702f6a-eedd-46df-8021-81afda069cc4" />

### Test Results 

<img width="506" height="58" alt="Screenshot 2026-04-12 at 8 46 33 PM" src="https://github.com/user-attachments/assets/1c71bfa9-108d-4314-b89f-ef6f08aee240" />

### Tests and Coverage Per Agent

**Flashcard Agent (Issue #3):**
- Tests written: 12
- Status: PASSING

<img width="582" height="97" alt="Screenshot 2026-04-12 at 8 49 19 PM" src="https://github.com/user-attachments/assets/5c816565-e671-4e59-b22f-4059e885c5a8" />

**Summary Agent (Issue #4):**
- Tests written: 15
- Status: PASSING

<img width="928" height="115" alt="Screenshot 2026-04-12 at 8 51 04 PM" src="https://github.com/user-attachments/assets/142c1147-ec16-4121-8c66-382e8dda96bc" />

**Quiz Agent (Issue #31):**
- Tests written: 34
- Status: PASSING

<img width="931" height="115" alt="Screenshot 2026-04-12 at 8 51 35 PM" src="https://github.com/user-attachments/assets/b3020696-e8b8-4bc0-b8c4-618f16b77aba" />

**Total:** 96 tests passing, 0 regressions

### File Structure (Evidence #6)
**Total new files created:** 22
- 3 prompt files (flashcard_prompt.py, summary_prompt.py, quiz_prompt.py)
- 3 agent files (flashcard_agent.py, summary_agent.py, quiz_agent.py)
- 3 model files
- 3 schema files
- 3 service files
- 3 router files
- 1 test file per agent (3 total)
<img width="688" height="437" alt="Screenshot 2026-04-12 at 8 52 15 PM" src="https://github.com/user-attachments/assets/5417990a-41f5-4992-8b02-c4792084e119" />

### API Endpoints (Evidence #7)

**Flashcard Endpoint:**
- POST /api/v1/modules/{module_id}/flashcards
- Status code: 201
- Response: List of flashcards with difficulty and bloom_level

**Summary Endpoint:**
- POST /api/v1/modules/{module_id}/summaries
- Status code: 201
- Request body: { "summary_level": "Brief|Standard|Detailed" }
- Response: Single summary with word_count and level

**Quiz Endpoint:**
- POST /api/v1/modules/{module_id}/quizzes
- Status code: 201
- Request body: { "difficulty_level": "Easy|Medium|Hard" }
- Response: Single quiz with 5-15 questions

<img width="383" height="133" alt="Screenshot 2026-04-12 at 8 56 12 PM" src="https://github.com/user-attachments/assets/7b234fb9-3e36-4226-8101-8eb4d8656304" />

### TDD Workflow: RED Phase 

**Example: Flashcard Agent RED**

Test file created with failing tests:

<img width="669" height="649" alt="Screenshot 2026-04-12 at 8 59 09 PM" src="https://github.com/user-attachments/assets/7249fb23-2839-4e1a-98e8-39804da3e5b6" />

### TDD Workflow: GREEN Phase 

**Implementation created for Flashcard Agent**

Files added:
- src/agents/flashcard_agent.py
- src/agents/prompts/flashcard_prompt.py
- src/models/flashcard.py
- src/schemas/flashcard.py
- src/services/flashcard_service.py
- src/routers/flashcards.py

Result: All tests PASSING

<img width="683" height="638" alt="Screenshot 2026-04-12 at 9 00 12 PM" src="https://github.com/user-attachments/assets/e6a8983e-13e3-437e-a25f-5233e896c3b6" />

### Design Decisions (Evidence #10)

**1. Dual-Input Architecture**
Each agent accepts:
- module_content (instructor materials)
- student_notes (student's personal notes)

This allows AI to synthesize both sources.

**2. Validation Strategy**
- Flashcard: Simple field validation (question, answer, difficulty, bloom_level)
- Summary: Word count bounds validation (50-500 words depending on level)
- Quiz: Complex validation (MC/SA ratio, exactly 4 options per MC, 5-15 questions)

**3. Storage Pattern**
- Flashcard: Individual rows per flashcard
- Summary: Single summary per generation
- Quiz: Single quiz with questions as JSON column

**4. Error Handling**
All agents validate before API call:
- Empty input → ValueError
- Invalid parameters → ValueError before Claude API call
- JSON parsing failures → ValueError with message

**5. Max Tokens**
- Flashcard: 2048 tokens
- Summary: 1024 tokens
- Quiz: 4096 tokens (largest due to question complexity)

<img width="723" height="246" alt="Screenshot 2026-04-12 at 9 02 15 PM" src="https://github.com/user-attachments/assets/9afa7034-b3b4-4f18-9cff-89e11b655a74" />
