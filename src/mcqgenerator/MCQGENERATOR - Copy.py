import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()
key = os.getenv("OPENAI_KEY")

if not key:
    raise ValueError("API key is missing. Please set the OPENAI_KEY in the .env file.")

llm = ChatOpenAI(api_key=key, model_name="gpt-3.5-turbo", temperature=0.3)

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "grade", "tone", "response_json"],
    template="""
    Text:{text}
    You are an expert MCQ maker. Given the above text, it is your job to \
    create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
    Make sure the questions are not repeated and check all the questions to be conforming the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
    Ensure to make {number} MCQs
    ### RESPONSE_JSON
    {response_json}
    """
)

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template="""
    You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
    You need to evaluate the complexity of the question and give a complete analysis of the quiz if the students
    will be able to understand the questions and answer them. Only use at max 50 words for complexity analysis. 
    If the quiz is not up to par with the cognitive and analytical abilities of the students,\
    update the quiz questions which need to be changed and adjust the tone such that it perfectly fits the student abilities.
    Quiz_MCQs:
    {quiz}

    Check from an expert English Writer of the above quiz:
    """
)

def generate_quiz(text, number, grade, tone, response_json):
    formatted_prompt = quiz_generation_prompt.format(
        text=text,
        number=number,
        grade=grade,
        tone=tone,
        response_json=response_json
    )
    return llm(formatted_prompt)

def evaluate_quiz(subject, quiz):
    formatted_prompt = quiz_evaluation_prompt.format(
        subject=subject,
        quiz=quiz
    )
    return llm(formatted_prompt)

def generate_and_evaluate_quiz(text, number, subject, tone, response_json):
    try:
        quiz_result = generate_quiz(text, number, subject, tone, response_json)
        quiz = json.loads(quiz_result)
        review_result = evaluate_quiz(subject, quiz)
        return quiz_result, review_result
    except Exception as e:
        return str(e), None
