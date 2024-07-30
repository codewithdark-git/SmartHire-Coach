import streamlit as st
from pages.interview import interview_chatbot
from utils.real_time_pipeline import RealTimePipeline


def main():
    st.set_page_config(page_title="SmartHire Coach", page_icon="🎓", layout="wide")
    st.title("SmartHire Coach 🎓")

    if 'pipeline' not in st.session_state:
        csv_file = 'question.csv'
        st.session_state.pipeline = RealTimePipeline(csv_file)

    if 'interview_type' not in st.session_state:
        st.session_state.interview_type = None

    st.sidebar.title("Interview Settings")
    interview_type = st.sidebar.radio(
        "Select Interview Type",
        ("General", "Technical", "Behavioral",), index=None,
        key="interview_type_selection"
    )

    if interview_type != st.session_state.interview_type:
        st.session_state.interview_type = interview_type
        reset_interview_state()

    if interview_type == "Technical":
        job_position = st.sidebar.text_input("Enter Job Position", key="job_position_input")
        if job_position:
            st.session_state.job_position = job_position

        question_type = st.sidebar.radio(
            "Question Type",
            ("Multiple Choice", "Open-ended"),index=None,
            key="question_type_selection"
        )
        st.session_state.question_type = question_type

    if st.sidebar.button("Start New Interview", key="start_new_interview"):
        reset_interview_state()
        st.rerun()

    interview_chatbot(st.session_state.pipeline, interview_type)


def reset_interview_state():
    keys_to_reset = ['job_position', 'chat_history', 'current_question_index',
                     'waiting_for_follow_up', 'interview_completed', 'question_type']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]


if __name__ == "__main__":
    main()