import streamlit as st
import random
import json
import time
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Step 1: Set up the Google API key

# Step 1: Load environment variables from the .env file
load_dotenv()  # This will load the .env file automatically

# Step 2: Get the Google API key from the environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if the API key was loaded correctly
if not GOOGLE_API_KEY:
    st.error("Google API key not found. Please check your .env file.")
    st.stop()


# ... Rest of your code remains unchanged

# Step 2: Initialize the LLM Model (Gemini or Text-Bison)
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # Use "text-bison@001" if needed
        api_key=GOOGLE_API_KEY,
        temperature=0.5,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    st.sidebar.success("✅ LLM initialized successfully!")
except Exception as e:
    st.sidebar.error(f"❌ Error initializing LLM: {e}")
    st.stop()

# Step 3: Define MCQ Prompt Template
mcq_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a multiple-choice question (MCQ) generator focused on English proficiency. "
                "Generate exactly 10 unique questions, each with 4 answer options (A, B, C, D). "
                "Ensure that each question only has one correct answer. "
                "Return only the result in JSON format."
            ),
        ),
        (
            "human",
            "Generate 10 multiple-choice questions. Return the result as a JSON array like this:\n"
            "[\n"
            '  {{ "question": "What is the synonym of \'happy\'?",\n'
            '    "options": ["A) Sad", "B) Angry", "C) Joyful", "D) Tired"],\n'
            '    "answer": "C" }},\n'
            "  ...\n"
            "]"
        ),
    ]
)

# Chain the LLM with the prompt
mcq_chain = mcq_prompt | llm

# Function to Generate MCQs (Only Once)
def generate_mcqs():
    try:
        response = mcq_chain.invoke({})  # Invoke the chain

        if not response or not response.content:
            st.error("The API returned an empty response. Please try again later.")
            return []

        raw_text = response.content.strip()
        st.write(f"Debug: Raw MCQ Response:\n{raw_text}")  # Optional Debugging

        if raw_text.startswith("[") and raw_text.endswith("]"):
            questions = json.loads(raw_text)
            random.shuffle(questions)  # Shuffle questions for randomness
            return questions
        else:
            raise ValueError("Invalid JSON format received.")

    except (json.JSONDecodeError, ValueError) as e:
        st.error(f"Error decoding JSON: {e}")
        return []
    except Exception as e:
        st.error(f"Error generating MCQs: {e}")
        return []

# Initialize session state to store questions, answers, and score
if "questions" not in st.session_state:
    st.session_state.questions = []
if "user_responses" not in st.session_state:
    st.session_state.user_responses = [""] * 10  # Store 10 empty answers initially
if "score" not in st.session_state:
    st.session_state.score = 0

# Function to Display the Quiz
def display_quiz():
    questions = st.session_state.questions

    if questions:
        st.header("📝 Quiz Time! Answer All Questions Below:")
        for i, q in enumerate(questions):
            st.write(f"**Question {i + 1}:** {q['question']}")
            for option in q["options"]:
                st.write(option)

            # Store the user input in session state
            answer = st.text_input(f"Your answer for Q{i + 1} (A/B/C/D):", key=f"answer-{i}")
            st.session_state.user_responses[i] = answer.upper()  # Store in session state

        if st.button("Submit Quiz"):
            evaluate_quiz()

# Function to Evaluate the Quiz and Show Results
def evaluate_quiz():
    questions = st.session_state.questions
    user_responses = st.session_state.user_responses
    score = 0

    for i, q in enumerate(questions):
        if user_responses[i] == q["answer"]:
            score += 1

    st.write(f"\nYou scored **{score} out of {len(questions)}**!")

    # Assess the user's proficiency level
    level = assess_level(user_responses)
    st.write(f"Your English proficiency level is: **{level}**")

    # Show feedback based on the score
    if score == len(questions):
        st.balloons()
        st.success("🎉 Perfect Score! You're an English wizard!")
    elif score > len(questions) * 0.7:
        st.info("Great job! You have a solid understanding of English.")
    elif score > len(questions) * 0.4:
        st.warning("Good effort! Keep practicing and you'll get even better.")
    else:
        refer_to_tutor()

# Function to Assess User's Proficiency Level
def assess_level(user_responses):
    try:
        assessment_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Evaluate the user’s responses to the English quiz and determine their proficiency level. "
                        "Provide only one of the following levels: Beginner, Intermediate, Good, or Expert."
                    ),
                ),
                (
                    "human",
                    f"User Responses: {user_responses}\n"
                    "Return only the proficiency level."
                ),
            ]
        )

        assessment_chain = assessment_prompt | llm
        response = assessment_chain.invoke({"responses": user_responses})

        if not response or not response.content:
            raise ValueError("Empty response from the evaluation API")

        return response.content.strip()

    except Exception as e:
        st.error(f"Error assessing proficiency: {e}")
        return "Unknown"

# Function to Refer to Tutor for Low Scores
def refer_to_tutor():
    st.info(
        "It looks like you’re finding English a bit tricky, but don’t worry—I’ve got a solution for you. 😊\n"
        "I highly recommend an English course with an expert tutor, **Professor Ishq**, from **Task Academy, Multan**.\n"
        "He’s known for helping students just like you achieve their full potential.\n"
        "With Prof. Ishq guiding you, you’ll become confident in English in no time! 🎯"
    )

# Display Main Options in Streamlit
def show_options():
    st.title("Taksa - Your Friendly English Expert 🧠✨")
    st.write(
        "Hello! I'm Taksa, your friendly English expert. Whether you want to test your English proficiency or just have a chat, I’m here for you!"
    )
    st.write("- **If you’d like to check your English level, please click 'Start Quiz' below.**")
    st.write("- **Curious to know more about me? Click 'Introduce Yourself'.**")
    st.write("- **Not in the mood? Click 'Exit' to leave.**")

# Main Function to Control Navigation
def main():
    show_options()
    menu_choice = st.sidebar.radio("Navigation", ["Home", "Start Quiz", "Introduce Yourself", "Exit"])

    if menu_choice == "Home":
        st.write("Welcome! Choose an option from the sidebar to get started.")
    elif menu_choice == "Start Quiz":
        if not st.session_state.questions:
            st.session_state.questions = generate_mcqs()  # Generate questions only once
        display_quiz()
    elif menu_choice == "Introduce Yourself":
        st.write(
            "Hi! I am Taksa, a little creation brought to life by someone very special: Muhammad Adnan. "
            "He is a passionate student of Electrical Engineering at NUST. But beyond his studies, Adnan poured his heart "
            "into building me—not just as a technical project, but as a meaningful gift. He named me after someone who means the world to him—his Queen. "
            "Adnan wanted to gift me to her on her birthday, as a token of his love and admiration. Every word I speak and every answer I give carries a little "
            "bit of the thought and care he put into making me, just for her."
         )
    elif menu_choice == "Exit":
        st.write("Goodbye! See you next time. 😊")

# Run the Streamlit App
if __name__ == "__main__":
    main()



