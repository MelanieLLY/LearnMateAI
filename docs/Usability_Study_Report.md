# LearnMateAI Usability Study Report - Simplified Version

**Authors:** Jing, LiuYi

**Note:** Video recordings are available. Access the full document at john.guerra@gmail.com

---

## 1. What is LearnMateAI?

**What it does:** LearnMateAI is a learning platform that uses AI to help students. It creates flashcards, quizzes, and summaries from course materials and student notes.

**Who uses it:** University students who want AI tools to help them study better.

**What data it stores:** Course modules, uploaded materials (PDFs, documents), student notes, AI-generated content, user information, and quiz results.

---

## 2. Three Main Tasks Tested

- **Task 1 (Browse & Navigate):** Log in, find the course module, and read the material using the split-screen layout.
- **Task 2 (Generate & Interact):** Create AI flashcards and study them.
- **Task 3 (Assess & Feedback):** Take an AI quiz, use hints, submit answers, and see your score with feedback.

---

## 3. How We Tested

**Before Testing:**
- Welcomed participants and explained the study
- Asked permission to record
- Reminded them this is not a test of them
- Asked them to think out loud

**Questions About Participants:**
- What is your role (student or teacher)?
- How often do you use learning apps (daily, weekly, or monthly)?
- Have you used AI learning tools before?

**Recording:** Video and screen recording were turned on.

**What We Asked Participants to Do:**
- **First:** Look at the homepage and tell us what you think the app does
- **Task 1:** Log in as a student, find "Intro to Machine Learning," and open the PDF. What do you think about how it looks?
- **Task 2:** Create flashcards and study them like you're preparing for a test
- **Task 3:** Take a quiz, try using the hint feature, answer questions, and check your results

**Questions After Testing (Rate 1-5, where 1 = Strongly Disagree, 5 = Strongly Agree):**
- Was Task 1 effective?
- Was Task 1 easy to use?
- Was Task 2 effective?
- Was Task 2 easy to use?
- Was Task 3 effective?
- Was Task 3 easy to use?
- Was the app effective overall?
- Was the app easy to use overall?
- Any other comments or suggestions?

---

## 4. What We Learned From Each Student

### Student 1 - Sophomore Computer Science Major

**Video:** https://youtu.be/g4xopW8tMpQ?si=_v2qU1syU1__ll9z

**Main Points:**
- Quickly understood the app (it looks like Notion)
- Liked the split-screen layout
- Found the module very quickly - no problems
- **Problem with Task 2:** When creating flashcards, the app took 2-3 seconds to respond but showed no loading sign. The student thought it was broken and clicked again. Said: "You need a loading spinner here."
- Task 3 went smoothly, but the student wanted to choose quiz difficulty level

**Scores:**
- Task 1: Effective (5/5), Easy (5/5)
- Task 2: Effective (4/5), Easy (3/5)
- Overall: Effective (4.5/5), Easy (4/5)

**Suggestion:** Add a loading indicator when the AI is working.

---

### Student 2 - Junior Humanities Major

**Main Points:**
- Thought it looked like an advanced version of Canvas
- Task 1 was okay once they found the material link
- Really liked the 3D flashcards
- **Problem with Task 2:** Had to click small arrows to move between flashcards. Said: "I wish I could just use arrow keys on my keyboard."
- Task 3: Tried the hint feature but felt it gave away the answer instead of helping them think. Also said the example materials in the app feel too simple.

**Scores:**
- Task 1: Effective (4/5), Easy (4/5)
- Task 2: Effective (5/5), Easy (3.5/5)
- Overall: Effective (4.5/5), Easy (4/5)

**Suggestions:** Add keyboard shortcuts for flashcards and use better example materials.

---

### Student 3 - Senior Student (Heavy AI Tool User)

**Main Points:**
- Understood the AI learning idea right away
- Used a small 13-inch laptop
- **Problem with Task 1:** Said the split-screen layout was cramped on the small screen. The PDF column was too narrow.
- Task 2: Liked the quality but wanted a "Regenerate" button to get different summaries
- Task 3: Liked the quiz but wanted to save quiz results to see progress over time. Said: "It would be great to see my quiz history on a dashboard."

**Scores:**
- Task 1: Effective (4/5), Easy (4/5)
- Task 3: Effective (4/5), Easy (4/5)
- Overall: Effective (4/5), Easy (4/5)

**Suggestions:** Add quiz history feature and make the layout work better on small screens.

---

## 5. Problems Found and How We Fixed Them

### Problem 1: No Loading Sign When AI is Working
**What we did:** Add a loading animation (skeleton UI) while the app is creating content.  
**How important:** MUST FIX  
**Done?** YES - We added a skeleton screen when `isGenerating` is true.

### Problem 2: Can't Use Keyboard to Flip Flashcards
**What we did:** Add support for arrow keys to move between flashcards.  
**How important:** SHOULD FIX  
**Done?** YES - We added keyboard event listeners to the flashcard component.

### Problem 3: Split-Screen Too Cramped on Small Screens
**What we did:** Let users hide the left sidebar or resize the columns.  
**How important:** COULD FIX  
**Done?** YES - We added a button to collapse the sidebar for more reading space.

### Problem 4: Example Materials Too Simple
**What we did:** Add better, more detailed example course materials to the app.  
**How important:** WOULD BE NICE  
**Done?** NOT YET - This is planned for later when we prepare data for the real launch.
