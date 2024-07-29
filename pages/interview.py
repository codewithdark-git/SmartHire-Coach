import streamlit as st
import random


def interview_chatbot(pipeline, interview_type):
    st.header(f"{interview_type} Interview Practice")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for idx, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if 'waiting_for_follow_up' not in st.session_state:
        st.session_state.waiting_for_follow_up = False

    job_position = st.session_state.get('job_position') if interview_type == "Technical" else None
    questions = pipeline.fetch_questions(interview_type, job_position)

    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]

        if not st.session_state.waiting_for_follow_up:
            display_question(current_question, interview_type)

            user_answer = get_user_answer(current_question, interview_type)

            if user_answer is not None:
                process_user_answer(pipeline, current_question, user_answer)
                st.experimental_rerun()

        else:
            handle_follow_up_question()

    if st.session_state.current_question_index >= len(questions):
        display_interview_completion(pipeline)


def display_question(question, interview_type):
    with st.chat_message("assistant"):
        st.markdown(question['question'])
    st.session_state.chat_history.append({"role": "assistant", "content": question['question']})

    if interview_type == "Technical" and st.session_state.get('question_type') == "Multiple Choice":
        options = question.get('options', [])
        if options:
            st.markdown("Please select your answer:")
            for option in options:
                st.markdown(f"- {option}")


def get_user_answer(question, interview_type):
    if interview_type == "Technical" and st.session_state.get('question_type') == "Multiple Choice":
        options = question.get('options', [])
        if options:
            return st.radio("Your answer:", options, key=f"mc_answer_{st.session_state.current_question_index}")
    else:
        return st.chat_input("Your answer")


def process_user_answer(pipeline, question, user_answer):
    with st.chat_message("user"):
        st.markdown(user_answer)
    st.session_state.chat_history.append({"role": "user", "content": user_answer})

    feedback = pipeline.process_answer(question, user_answer)

    with st.chat_message("assistant"):
        st.markdown(feedback)
    st.session_state.chat_history.append({"role": "assistant", "content": feedback})

    follow_up_question = pipeline.generate_follow_up_question(question, user_answer)
    with st.chat_message("assistant"):
        st.markdown(f"**Follow-Up Question:** {follow_up_question}")
    st.session_state.chat_history.append(
        {"role": "assistant", "content": f"**Follow-Up Question:** {follow_up_question}"})

    st.session_state.waiting_for_follow_up = True


def handle_follow_up_question():
    follow_up_answer = st.chat_input("Your answer to the follow-up question")

    if follow_up_answer:
        with st.chat_message("user"):
            st.markdown(follow_up_answer)
        st.session_state.chat_history.append({"role": "user", "content": follow_up_answer})

        st.session_state.current_question_index += 1
        st.session_state.waiting_for_follow_up = False


def display_interview_completion(pipeline):
    st.session_state.interview_completed = True
    with st.chat_message("assistant"):
        overall_feedback = pipeline.generate_overall_feedback(st.session_state.chat_history)
        st.markdown(overall_feedback)

    if st.button("View Detailed Feedback"):
        display_detailed_feedback(pipeline)


def display_detailed_feedback(pipeline):
    st.subheader("Detailed Feedback")
    for idx, qa_pair in enumerate(zip(st.session_state.chat_history[::2], st.session_state.chat_history[1::2])):
        question, answer = qa_pair
        st.markdown(f"**Question {idx + 1}:** {question['content']}")
        st.markdown(f"**Your Answer:** {answer['content']}")
        feedback = pipeline.process_answer({"question": question['content']}, answer['content'])
        st.markdown(f"**Feedback:** {feedback}")
        st.markdown("---")