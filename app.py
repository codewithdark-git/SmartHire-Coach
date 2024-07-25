import streamlit as st
from ulits.response import generate_text


st.title('AI-Powered Job Interview Coach')

# Interview Questions
interview_questions = [
    "Tell me about yourself.",
    "Why do you want to work here?",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in 5 years?",
    "Describe a challenging situation you faced and how you dealt with it."
]

st.header("Mock Interview")
question = st.selectbox("Select a question to answer:", interview_questions)
answer = st.text_area("Your Answer:")

if st.button("Get Feedback"):
    feedback_prompt = f"Provide feedback on this interview answer: '{answer}'"
    feedback = generate_text(feedback_prompt)
    st.text_area("Feedback", feedback)
