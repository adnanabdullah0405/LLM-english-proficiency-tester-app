# LLM-english-proficiency-tester-app
A Generative AI app using Gemini LLM to assess English proficiency. It generates MCQs, evaluates responses, scores the user, provides personalized feedback, and recommends a teacher if needed. Includes a Streamlit GUI and is fully deployed.

##  Overview

This is a **Generative AI project** powered by **Gemini LLM**, designed to assess a user's English proficiency in real time. The system generates a set of grammar and comprehension-based MCQs, evaluates user responses, scores their proficiency, and provides **personalized feedback and learning recommendations** — all through a user-friendly **Streamlit GUI**.

---

##  Objective

To build an interactive AI-based English testing platform that:
1. Generates dynamic English MCQs using an LLM
2. Collects and evaluates user answers via a second LLM
3. Scores the user and classifies proficiency level
4. Provides personalized feedback and tutor recommendations if needed

---

###  LLM Pipeline

[Generator LLM]
↓ (Generates MCQs)
[User Interface - Streamlit]
↓ (User completes the quiz)
[Evaluator LLM]
↓ (Evaluates answers & scores)
[Feedback & Recommendation Engine]


- **Generator LLM**: Produces 10 English MCQs (grammar, comprehension, vocabulary)
- **Evaluator LLM**: Compares answers and calculates score
- **Recommendation Engine**:
  - If score < 50%, recommends a tutor or improvement resource
  - Gives constructive feedback

---

## 💻 GUI (Streamlit App)

The user interface allows:
- One-click generation of MCQs
- Real-time form-based submission
- Display of results and proficiency level
- Feedback messages and recommendations

![App Screenshot](path/to/your/screenshot.png)

---
