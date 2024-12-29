import os
import streamlit as st
import pandas as pd
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate

# Configure Gemini API
os.environ['some_key'] = st.secrets['some_key'] =api_key 

genai.configure(api_key=api_key)
llm = genai.GenerativeModel("gemini-1.5-flash")


def get_1st_question(data):
    Prompt_template = """{data}, You are a career guidance AI designed to help users discover their ideal career paths through psychological analysis. Begin by asking the user a series of open-ended questions..."""
    prompt = PromptTemplate.from_template(Prompt_template)
    formatted_prompt = prompt.format(data=data)
    try:
        response = llm.generate_content(formatted_prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")
        return ""


def get_dynamic_question(previous_answers):
    prompt_template = """
    Given the previous answers: {answers}, generate the next question to better understand the individual's career preferences and personality.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    formatted_prompt = prompt.format(answers=previous_answers)
    try:
        response = llm.generate_content(formatted_prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating dynamic question: {str(e)}")
        return ""


def generate_recommendations(data):
    prompt_template = """
    Based on the following inputs: {data}, suggest three career options and explain why these careers would suit the individual.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    formatted_prompt = prompt.format(data=data)
    try:
        response = llm.generate_content(formatted_prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return ""


# Streamlit UI
st.title("Career Choice Correction (C-Cube)")
st.subheader("A simple prototype to explore your career options")

role = st.selectbox("Who are you?", ["Self", "Family", "Friend"])
st.write(f"Answer the questions from the perspective of: {role}")

if "questions" not in st.session_state:
    st.session_state.questions = []  
    st.session_state.answers = {}   

if not st.session_state.questions:
    initial_context = f"Starting context for {role}"
    first_question = get_1st_question(initial_context)
    st.session_state.questions.append(first_question)

current_question = st.session_state.questions[-1]
st.write(f"Q: {current_question}")
answer = st.text_input("Your Answer", key=f"answer_{len(st.session_state.answers)}")

if st.button("Submit Answer"):
    st.session_state.answers[current_question] = answer
    next_question = get_dynamic_question(st.session_state.answers)
    st.session_state.questions.append(next_question)

if st.button("Finish"):
    st.write("Collected Responses:", st.session_state.answers)
    st.subheader("Your Suggested Careers:")
    recommendations = generate_recommendations(st.session_state.answers)
    st.write(recommendations)

if st.button("Clear"):
    st.session_state.clear()

# About section
st.sidebar.title("About")
st.sidebar.write("""This prototype collects responses to generate basic career suggestions based on psychometric analysis.""")
