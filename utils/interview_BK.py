import streamlit as st


def interview_chatbot(pipeline, interview_type):
    st.header(f"{interview_type} Interview Practice")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if interview_type == "Technical":
        if 'user_info_collected' not in st.session_state or not st.session_state.user_info_collected:
            display_user_info_prompt()
            # Check if user info is correctly set
            if 'job_position' not in st.session_state or 'question_type' not in st.session_state:
                return  # Ensure to stop here until user info is provided

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    job_position = st.session_state.get('job_position') if interview_type == "Technical" else None

    questions = pipeline.fetch_questions(interview_type, job_position)

    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]

        user_answer = display_question_and_get_answer(current_question, interview_type)

        if user_answer:
            with st.spinner("Generating feedback..."):
                process_user_answer(pipeline, current_question, user_answer)

            st.session_state.current_question_index += 1
            st.rerun()
    else:
        display_interview_completion(pipeline)


def display_user_info_prompt():
    st.chat_message("assistant").markdown(
        "For the Technical interview, please provide the following information:"
        "\n1. **Job Position** (e.g., Software Engineer, Data Scientist)"
        "\n2. **Question Type** (Multiple Choice or Open-ended)"
    )

    job_position = st.text_input("Enter Job Position")
    question_type = st.radio("Select Question Type", ['Multiple Choice', 'Open-ended'], index=None)

    # Ensure both fields are filled
    if job_position and question_type:
        st.session_state.job_position = job_position
        st.session_state.question_type = question_type
        st.session_state.user_info_collected = True
        st.chat_message("user").markdown(
            f"The job position is **{st.session_state.job_position}** and the question type is **{st.session_state.question_type}**."
        )
    else:
        st.session_state.user_info_collected = False
        st.chat_message("assistant").markdown(
            "Please provide both a valid Job Position and Question Type to proceed."
        )


def display_question_and_get_answer(question, interview_type):
    with st.chat_message("assistant"):
        st.markdown(question['question'])
    st.session_state.chat_history.append({"role": "assistant", "content": question['question']})

    if interview_type == "Technical" and question.get('options'):
        st.markdown("Select Your answer:")
        user_answer = st.radio("", question['options'], key=f"mc_answer_{st.session_state.current_question_index}", index=None)
        return user_answer
    else:
        return st.chat_input("Your answer")


def process_user_answer(pipeline, question, user_answer):
    with st.chat_message("user"):
        st.markdown(user_answer)
    st.session_state.chat_history.append({"role": "user", "content": user_answer})

    feedback = pipeline.process_answer(question, user_answer)

    st.chat_message("assistant").markdown(f'####Feedback: {feedback}')
    st.session_state.chat_history.append({"role": "assistant", "content": feedback})


def display_interview_completion(pipeline):
    if 'interview_completed' not in st.session_state:
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
