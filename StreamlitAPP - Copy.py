import os
import json
import traceback
from dotenv import load_dotenv
import streamlit as st
from src.mcqgenerator.MCQGENERATOR import generate_and_evaluate_quiz
from src.mcqgenerator.logger import logging

load_dotenv()

st.title("MCQ Generator")

api_key = os.getenv("OPENAI_KEY")

if not api_key:
    st.error("API key is missing. Please set the OPENAI_KEY in the .env file.")
    st.stop()

with st.form(key='mcq_form'):
    text = st.text_area("Text for MCQ Generation")
    number = st.number_input("Number of Questions", min_value=1, max_value=50, value=5)
    subject = st.text_input("Subject")
    tone = st.text_input("Tone")
    response_json = st.text_area("Response JSON", "{}")

    submit_button = st.form_submit_button("Generate MCQs")

    if submit_button:
        try:
            quiz_result, review_result = generate_and_evaluate_quiz(
                text=text,
                number=number,
                subject=subject,
                tone=tone,
                response_json=response_json
            )

            st.subheader("Generated Quiz")
            st.json(quiz_result)

            st.subheader("Quiz Review")
            st.text(review_result)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            logging.error(traceback.format_exc())
