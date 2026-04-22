# Usability Study Report

**Note:** Video and screen recording can be accessed. This document is shared with john.guerra@gmail.com


## 1. What is LearnMateAI?

LearnMateAI is a learning app that uses AI to help students study. It makes quizzes for testing knowledge based on course materials and student notes.

**Users:** University students who want to test their knowledge and track learning progress.

**Data:** The app stores user accounts, modules, course materials, AI-generated quizzes, quiz scores, and answers.

---

## 2. What Feature Was Tested?

The user tested the **Quiz Feature** - the complete flow from account creation to quiz review:
1. Register a new account
2. Log in
3. Generate a quiz for a module
4. Take the quiz
5. Check the score
6. See why answers were wrong to learn

---

## 3. How The Study Was Done

### Before It Started

The user was asked:
- What year of study are you in?
- How often do you use study apps? (Daily/Weekly/Monthly)
- Do you know AI learning tools?

Video and screen were recorded.

### What The User Did

**Flow:**
"Create a new account. Log in. Go to the 'Intro to Machine Learning' module. Generate a quiz. Take the quiz and answer the questions. Submit and look at your score. Check which answers were wrong and see the explanations. Tell me what you think as you do it."

### Questions After (1=Strongly Disagree, 5=Strongly Agree)

- Was it easy to create an account and log in?
- Was it easy to generate a quiz?
- Was it easy to take the quiz?
- Was it easy to understand your score and wrong answers?
- Did the quiz help you learn?
- Was the whole flow easy to use?
- Any ideas to make it better?

---

## 4. What Happened

### User 1: https://youtu.be/g4xopW8tMpQ?si=CQ3ueQxUhFvWGSlj

**Background:** Junior computer science student, uses study apps 2-3 times a week, familiar with AI tools.

**What Happened:**
- Registered account easily. Login was smooth.
- Found the module and clicked "Generate Quiz" - quiz was created in 5 seconds.
- Took the quiz without any confusion. All questions were clear.
- Submitted the quiz and saw the score right away.
- Reviewed wrong answers and understood the explanations. Found it helpful to learn from mistakes.

**Quote:**
"The app is good. I like that I can see why I got answers wrong. But I wish there was a history section where I can see all my past quizzes and track my progress over time. That would be really useful."

**Scores:**
- Account & Login Easy: 5
- Generate Quiz Easy: 5
- Take Quiz Easy: 5
- Understand Score & Explanations Easy: 5
- Quiz Helped Learn: 5
- Overall Easy to Use: 5
- Overall Helpful: 5

**Main Feedback:** Good app. Needs quiz history to track progress.

---

### User 2: https://youtu.be/ORA8LX6rZCY?si=WzOc6Fk2D7a0kRjP

**Background:** Sophomore business student, uses study apps 3-4 times a week, familiar with some AI tools.

**What Happened:**
- Logged in quickly without any issues.
- Clicked "Generate Flashcard" for the same module.
- Waited for the flashcard to generate - took about 8-10 seconds.
- Started playing with the flashcards. Flipping between cards, reviewing content.
- Found the flashcard interaction very smooth and enjoyable.

**Quote:**
"The flashcards are really nice to use. Flipping through them is fun and easy. But the generation is a bit slow. When I clicked generate, I had to wait almost 10 seconds. It would be better if it was faster."

**Scores:**
- Login Easy: 5
- Generate Flashcard Easy: 4
- Play with Flashcard Easy: 5
- Understand Flashcard Content: 5
- Flashcard Helped Learn: 5
- Overall Easy to Use: 4.5
- Overall Helpful: 5

**Main Feedback:** Flashcards are fun and easy to use. Generation speed needs improvement.

---

## 5. Main Findings

**Positive from User 1:** The quiz feature works smoothly. Users can easily create an account, generate quizzes, take them, and learn from wrong answers.

**What's Missing from User 1:** Quiz history section. Users want to:
- See all past quizzes they took
- Track their progress over time
- Compare scores from different attempts

**Positive from User 2:** The flashcard feature is fun and easy to use. Playing with flashcards works great.

**What's Slow from User 2:** Flashcard generation takes 8-10 seconds. Users want it to be faster.

---

## 6. Next Steps

1. **For Quiz Feature:** Add a quiz history page where users can see:
   - List of all quizzes taken (with dates)
   - Score for each quiz
   - Option to retake old quizzes
   - Simple progress chart showing improvement over time

2. **For Flashcard Feature:** Speed up the generation process. Consider:
   - Optimize AI prompt processing
   - Use caching for similar content
   - Show progress indicator while generating
   
