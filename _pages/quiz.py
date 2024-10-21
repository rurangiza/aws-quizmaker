import streamlit as st

from srcs.llm import QuizMaker, Quiz, Question

from typing import Optional, List, Dict


##
## Function Definitions
##

def get_topic(placeholder) -> Optional[str | None]:
    with placeholder.container():
        if st.button('VPC', use_container_width=True, key=1):
            return 'VPC'
        if st.button('EC2', use_container_width=True, key=2):
            return 'EC2'
        if st.button('S3', use_container_width=True, key=3):
            return 'S3'
        if st.button('RDS & Aurora', use_container_width=True, key=4):
            return 'RDS & Aurora'
        if st.button('EC2 Instance Storage', use_container_width=True, key=5):
            return 'EC2 Instance Storage'
        return None

def create_card(question: Question):
    options = ['100', '53ou', 'Instance Storage', 'Nothing']
    with st.container(border=True):
        st.markdown('Pick between the following options. Which one is better?')
        user_answer = st.radio(label="", options=options)
        if st.button('Save', type='primary'):
            pass

def start_quiz(quiz: Quiz):
    questions = quiz.questions
    st.progress(value=0)
    for question in questions:
        create_card(question)


##
## State Variables
##

if 'quizmaker' not in st.session_state:
    st.session_state.quizmaker = QuizMaker()
if 'score_history' not in st.session_state:
    st.session_state.score_history = []
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key (gpt-4o-mini)")
    langchain_api_key = st.text_input('Langchain API Key')

##
## Variables
##

st.title("Quiz")

st.markdown('Welcome to Quizmaker, a Quiz generator app to prepare for the AWS Certified Developer exam.')
st.markdown("Pick a topic below and you'll get 10 quizes about that topic.")

body = st.empty()

# with body.container():
if (topic := get_topic(body)):
    body.empty()
    with st.spinner('Generating quiz'):
        st.session_state.quiz = st.session_state.quizmaker.invoke(topic)
    start_quiz(st.session_state.quiz)
    # st.success(f"You've selected{topic}")

if (topic := st.chat_input("Enter a topic you'd like to practice")):
    pass


create_card('')