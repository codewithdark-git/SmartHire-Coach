import streamlit as st

st.sidebar.title("AI-Powered Job Interview Coach")
page = st.sidebar.selectbox("Choose a page", ["Mock Interview", "Resume Review", "Job Search Assistance"])

if page == "Mock Interview":
    from interview import run_mock_interview
    run_mock_interview()
elif page == "Resume Review":
    from resume_review import run_resume_review
    run_resume_review()
elif page == "Job Search Assistance":
    from job_search_assistance import run_job_search_assistance
    run_job_search_assistance()

#
# # Footer
# st.markdown("<hr>", unsafe_allow_html=True)
# st.markdown("<footer><p style='text-align: center;'>AI-Powered Job Interview Coach © 2024</p></footer>", unsafe_allow_html=True)
