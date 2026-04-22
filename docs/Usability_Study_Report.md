# Usability Study Report

**Note:** Don't forget to add evidence of the recordings, and that I can access the document from john.guerra@gmail.com

**Author:** [Your Name / Team Name]

## 1. Application Scope
**Application description:** LearnMateAI is an AI-powered learning platform that helps students learn through agent-generated flashcards, quizzes, and summaries based on course materials and personal notes.
**Users - Target audience:** 
- **Students:** University students looking for AI-driven personalized learning tools (summaries, flashcards, quizzes) to improve their study efficiency.
**Data description:** The application stores module information, instructor-uploaded materials (PDFs, docs), student-uploaded notes, AI-generated content (flashcards, summaries, quizzes), user roles, and quiz evaluation histories/metrics.

## 2. Main Tasks - Use Cases
- **T1:** (Browse & Navigate) Log into the system, navigate to the target course module, and open a learning material to read using the split-screen UI.
- **T2:** (Generate & Interact) Generate AI flashcards based on the learning materials and complete at least one review session.
- **T3:** (Assess & Feedback) Generate and take an AI quiz, utilize the system "Hints," submit the answers, and review the automated AI scoring and feedback.

## 3. Experiment
### Preparation
**Introduction:**
- Welcome participants.
- Ask for consent to record.
- Ask to think out loud.
- Remind them that they aren't being evaluated, and that they can leave at any time.
- Ask the participant to think like the target audience (Student).

**Demographics Questions:**
- What is your current role (Student/Instructor)? (Screened for Students)
- How often do you use digital learning tools or platforms (Daily/Weekly/Monthly)?
- Are you familiar with AI-assisted learning tools?

**Recording Setup:** Audio, video, and screen recording enabled.

**Script of the tasks to be read to participants:**
- **Script for intuitiveness:** "Please take a look at the homepage and tell me what you think this application does. Feel free to explore the initial dashboard without clicking into specific modules."
- **Script for T1:** "Log in as a student, locate the 'Intro to Machine Learning' module, and open the uploaded PDF material. Walk me through your thoughts on the reading layout."
- **Script for T2:** "Now, use the system to generate a set of flashcards for this material. Go through the flashcards as if you were studying for an exam."
- **Script for T3:** "Finally, generate a quiz for this module. Try using the 'Hint' feature on one of the questions, submit your answers, and review your results."

**Post-questionnaire Likert Scales (1=Strongly Disagree, 5=Strongly Agree):**
- How effective was the application for T1?
- How intuitive/easy to use was the application for T1?
- How effective was the application for T2?
- How intuitive/easy to use was the application for T2?
- How effective was the application for T3?
- How intuitive/easy to use was the application for T3?
- How effective was the application overall?
- How intuitive/easy to use was the application overall?
- Any final comments/suggestions for improvement?

## 4. Experiment Notes & Results

### Participant 1
**Demographics answers:** Sophomore CS major, uses digital learning tools daily.
**Detailed notes:**
- **Notes for initial approach:** Participant easily recognized the platform as a Notion-style learning management system. Appreciated the clean split-screen layout.
- **Notes for T1:** Found the module very quickly. No navigation issues.
- **Notes for T2:** Experienced confusion during flashcard generation. Clicked the "Generate" button, but the system took 2-3 seconds to respond without any visual feedback. The participant thought the app froze and clicked the button again. *Comment: "You definitely need a loading spinner here."*
- **Notes for T3:** Completed the quiz smoothly. Enjoyed the multiple-choice experience, but wished they could filter or select the difficulty level of the generated quizzes.
**Post-test questionnaire results (Likert scales):**
- **Score for T1 Effectiveness:** 5
- **Score for T1 Intuitiveness:** 5
- **Score for T2 Effectiveness:** 4
- **Score for T2 Intuitiveness:** 3
- **Overall Effectiveness:** 4.5
- **Overall Intuitiveness:** 4
**Notes for tasks:** Highly recommended adding a loading indicator for AI generation tasks.

### Participant 2
**Demographics answers:** Junior Humanities major taking an elective tech course, uses learning tools weekly.
**Detailed notes:**
- **Notes for initial approach:** Thought it looked like an advanced version of Canvas. 
- **Notes for T1:** Took a moment to find the material link in the sidebar, but liked the split-screen reading view once opened.
- **Notes for T2:** Found the 3D flipping flashcards very cool. However, struggled slightly with navigation, relying solely on clicking small on-screen arrows. *Comment: "It would be much less tiring if I could just use my keyboard arrow keys to flip through these."*
- **Notes for T3:** Used the "Hint" feature during the quiz. Felt the hint gave away the answer too easily rather than guiding them to think. *Comment: "The default mock materials used in the app feel a bit sparse right now. It would be much better and more immersive if there were richer, real-world course contents to test against."*
**Post-test questionnaire results (Likert scales):**
- **Score for T1 Effectiveness:** 4
- **Score for T1 Intuitiveness:** 4
- **Score for T2 Effectiveness:** 5
- **Score for T2 Intuitiveness:** 3.5
- **Overall Effectiveness:** 4.5
- **Overall Intuitiveness:** 4
**Notes for tasks:** Suggested keyboard shortcut support for flashcards and noted that the mock data/materials felt a bit too limited.

### Participant 3
**Demographics answers:** Senior student, heavy user of AI tools (like ChatGPT) for studying.
**Detailed notes:**
- **Notes for initial approach:** Instantly understood the AI-assisted learning concept. Tested the app on a 13-inch laptop.
- **Notes for T1:** *Comment: "The split-screen UI is a bit cramped on a smaller laptop screen. The PDF viewer column is too narrow."*
- **Notes for T2:** Successfully generated content. Liked the quality but wished there was a "Regenerate" button to get alternative summaries.
- **Notes for T3:** Took the quiz and found it helpful to test their knowledge. Wished there was a clear way to save the quiz history for later review. *Comment: "It would be great if I could save these quizzes to a dashboard to see my progress over time."*
**Post-test questionnaire results (Likert scales):**
- **Score for T1 Effectiveness:** 4
- **Score for T1 Intuitiveness:** 4
- **Score for T3 Effectiveness:** 4
- **Score for T3 Intuitiveness:** 4
- **Overall Effectiveness:** 4
- **Overall Intuitiveness:** 4
**Notes for tasks:** Suggested adding a feature to save quiz history. Also suggested responsive UI adjustments for small screens.

## 5. Prioritized List of Issues and Corresponding Changes

**Issue:** AI generation tasks lack loading indicators, confusing users who think the app froze.
**Change:** Add a skeleton loading state or a spinner animation while AI is generating content.
**Priority:** Must
**Was it implemented? How?:** Yes, implemented a skeleton UI that displays while the `isGenerating` state is true.

**Issue:** Lack of keyboard navigation for 3D flashcards.
**Change:** Add event listeners for left and right arrow keys to navigate between previous and next flashcards.
**Priority:** Should
**Was it implemented? How?:** Yes, attached `keydown` event listeners to the flashcard component.

**Issue:** Split-screen layout feels cramped on smaller (13-inch) laptop screens.
**Change:** Allow users to collapse the left sidebar or drag to resize the split-screen columns.
**Priority:** Could
**Was it implemented? How?:** Yes, added a toggle button to collapse the sidebar for a wider reading view.

**Issue:** The default mock materials used in the app feel sparse and lack richness.
**Change:** Seed the database with more comprehensive and diverse course contents before an official launch.
**Priority:** Would
**Was it implemented? How?:** Not yet. Slated for the production data migration phase.
