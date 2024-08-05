import streamlit as st
from utils.interview_BK import interview_chatbot
from utils.real_time_pipeline import RealTimePipeline

# Mock implementation for demo
class MockPipeline:
    def fetch_questions(self, interview_type, job_position):
        return [{"question": "What is polymorphism in OOP?"}] if interview_type == "Technical" else []

    def process_answer(self, question, user_answer):
        return "Good answer."

    def generate_overall_feedback(self, chat_history):
        return "Overall, you performed well."


def main():
    st.set_page_config(page_title="SmartHire Coach", page_icon="🎓", layout="wide")
    st.title("SmartHire Coach 🎓")

    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = RealTimePipeline()

    if 'interview_type' not in st.session_state:
        st.session_state.interview_type = None

    st.sidebar.title("Interview Settings")
    interview_type = st.sidebar.radio(
        "Select Interview Type",
        ("General", "Technical"),
        key="interview_type_selection"
    )

    if interview_type != st.session_state.interview_type:
        st.session_state.interview_type = interview_type
        reset_interview_state()

    if interview_type is None:
        st.chat_message("assistant").write("Please select an interview type from the sidebar to begin.")
    elif interview_type == "General":
        st.chat_message("assistant").write("You've selected the **General** interview type. Please proceed with the general questions.")
    elif interview_type == "Technical":
        st.chat_message("assistant").write("You've selected the **Technical** interview type. Please provide the necessary details and proceed.")

    if st.sidebar.button("Start New Interview", key="start_new_interview"):
        reset_interview_state()
        st.rerun()

    if interview_type:
        interview_chatbot(st.session_state.pipeline, interview_type)

def reset_interview_state():
    keys_to_reset = ['job_position', 'chat_history', 'current_question_index',
                     'user_info_collected', 'interview_completed', 'question_type']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

if __name__ == "__main__":
    main()
