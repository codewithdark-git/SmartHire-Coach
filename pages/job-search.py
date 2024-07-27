import streamlit as st
from utils.response import generate_text


st.header("Job Search Assistance")

if st.button("Get Job Search Tips"):
    tag = st.text_input("Enter a job tag:")
    tips_prompt = "Provide some tips for {tag}job searching."
    job_search_tips = generate_text(tips_prompt)
    st.text_area("Job Search Tips", job_search_tips)

st.header("Job Matching")
job_description = st.text_area("Enter a job description:")

if st.button("Get Matching Jobs"):
    matching_jobs_prompt = f"Provide some job matching this description: {job_description}"
    matching_jobs = generate_text(matching_jobs_prompt)
    st.text_area("Matching Jobs", matching_jobs)

st.header("Interview Question Suggestions")
job_title = st.text_input("Enter a job title:")

if st.button("Get Interview Questions"):
    questions_prompt = f"Provide some common interview questions for a {job_title} position."
    interview_questions = generate_text(questions_prompt)
    st.text_area("Interview Questions", interview_questions)