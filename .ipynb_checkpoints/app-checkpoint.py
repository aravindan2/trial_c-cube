import streamlit as st
import pandas as pd
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate

# Configure Gemini API
api_key = "AIzaSyC_0zV2_iWEe0F58MAisYtdYUwipzIsPIE"
genai.configure(api_key=api_key)
llm = genai.GenerativeModel("gemini-1.5-flash")


# Function to get the next question dynamically
def get_dynamic_question(previous_answers):
    """
    Generate a new question based on previous answers using the Gemini API.
    """
    prompt_template = """
    Given the previous answers: {answers}, generate the next question 
    to better understand the individual's career preferences and personality.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    formatted_prompt = prompt.format(answers=previous_answers)
    response = llm.generate_content(formatted_prompt)
    
    return response.text.strip()


# Function for generating career recommendations
def generate_recommendations(data):
    """
    Generate career recommendations based on collected data using the Gemini API.
    """
    prompt_template = """
    Based on the following inputs: {data}, suggest three career options and explain why 
    these careers would suit the individual.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    formatted_prompt = prompt.format(data=data)
    response = llm.generate_content(formatted_prompt)

    return response.text.strip()


# Streamlit UI
st.title("Career Choice Correction (C-Cube)")
st.subheader("A simple prototype to explore your career options")

# Role input
role = st.selectbox("Who are you?", ["Self", "Family", "Friend"])
st.write(f"Answer the questions from the perspective of: {role}")

# Initialize session state for dynamic questions and answers
if "questions" not in st.session_state:
    st.session_state.questions = []  # List to store questions
    st.session_state.answers = {}   # Dictionary to store answers

# Generate the first question dynamically if none exist
if not st.session_state.questions:
    initial_context = f"Starting context for {role}"
    first_question = get_dynamic_question(initial_context)
    st.session_state.questions.append(first_question)

# Display current question and collect answer
current_question = st.session_state.questions[-1]
st.write(f"Q: {current_question}")
answer = st.text_input("Your Answer", key=f"answer_{len(st.session_state.answers)}")

if st.button("Submit Answer"):
    # Save the current answer
    st.session_state.answers[current_question] = answer

    # Generate the next question based on the current answers
    next_question = get_dynamic_question(st.session_state.answers)
    st.session_state.questions.append(next_question)

# Show submitted answers
if st.button("Finish"):
    st.write("Collected Responses:", st.session_state.answers)
    
    # Generate career recommendations
    st.subheader("Your Suggested Careers:")
    recommendations = generate_recommendations(st.session_state.answers)
    st.write(recommendations)

# About section
st.sidebar.title("About")
st.sidebar.write("""
This prototype collects responses from you, your family, and your friends 
to generate basic career suggestions based on psychometric analysis.
""")
