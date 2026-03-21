# LearnMateAI Sprint Plan

> 3 sprints · 2 developers · ~1 week each
> Deadline: Apr 19

---

## Sprint 1: Foundation + Module System (Mar 24 – Mar 30)

**Day 1-2: Person A solo — scaffolding**
- Next.js + FastAPI project setup, folder structure, DB schema
- Auth system: JWT login/register, role-based middleware (student / instructor / admin)
- GitHub org + repos, CI/CD pipeline (GitHub Actions: lint + test on PR)
- CLAUDE.md written (for HW4)
- Team contract established

**Day 3-7: Both devs in parallel**

| Person A | Person B |
|---|---|
| **Feature: Instructor module management** | **Feature: Student module experience** |
| Create/edit/delete module (API + UI) | Student module list + browse UI |
| Upload materials to S3 (API + UI) | View/download materials page |
| Define learning objectives per module | Student note upload (API + UI) |

**Sprint 1 deliverables:**
- Auth flow end-to-end
- Instructor creates module, uploads PDF, sets objectives
- Student browses modules, views materials, uploads personal notes
- CI/CD: auto test + deploy to dev on merge
- CLAUDE.md + team contract

---

## Sprint 2: AI Core Features (Mar 31 – Apr 6)

| Person A | Person B |
|---|---|
| **Feature: AI content generation + eval** | **Feature: Quiz & feedback loop** |
| Context builder: merge materials + notes | Quiz-taking UI (MCQ + open-ended) |
| 3 parallel agents (summary / flashcard / quiz) | Quiz submission API + answer storage |
| Summary display page | AI feedback on quiz answers (heuristic hints) |
| Flashcard display page | Quiz results page with score + explanations |
| LLM-as-judge eval system | Eval quality badge display on generated content |
| Store eval history in DB | |

**Sprint 2 deliverables:**
- "Generate study content" triggers 3 agents in parallel
- Summary, flashcards, quiz all render correctly
- Student takes quiz, gets AI feedback and hints
- Eval engine auto-scores every generation, history stored
- CI/CD: add staging environment

---

## Sprint 3: Reports, Production & Polish (Apr 7 – Apr 15)

| Person A | Person B |
|---|---|
| **Feature: Instructor report** | **Feature: Admin dashboard** |
| Aggregated class report API (anonymous stats) | Admin user management (API + UI) |
| Report dashboard UI (common gaps, avg scores) | Eval history dashboard + trend charts |
| | |
| **Then split remaining work:** | |
| Sentry + Grafana setup | UI polish (loading states, responsive) |
| Security (rate limiting, OWASP, secrets) | Documentation (README, API docs, blog post) |
| CI/CD: canary/blue-green deploy to prod | Presentation slides |

**Sprint 3 deliverables:**
- Instructor anonymous class performance report
- Admin user management + eval trend graphs
- Sentry + Grafana dashboards live
- Security hardened, production deployed
- Documentation package complete

---

## Apr 16 – Apr 19: Buffer

- Rehearse 20-min presentation
- Individual reflections + peer evaluations
- Bug fixes only, no new features
