import streamlit as st


def interview_chatbot(pipeline, interview_type):
    st.header(f"{interview_type} Interview Practice")

    # Initialize session state variables if they don't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    # Ensure user info is collected before proceeding
    if interview_type == "Technical":
        if 'user_info_collected' not in st.session_state or not st.session_state.user_info_collected:
            display_user_info_prompt()
            # return  # Stop execution here until user info is collected

    # Display all previous chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Determine job position if the interview type is Technical
    job_position = st.session_state.get('job_position') if interview_type == "Technical" else None

    # Fetch questions based on interview type and job position
    questions = pipeline.fetch_questions(interview_type, job_position)

    # Ensure current question index is within the range of questions
    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]

        # Display the current question and get the user's answer
        user_answer = display_question_and_get_answer(current_question, interview_type)

        # If the user has provided an answer, process it
        if user_answer:
            process_user_answer(pipeline, current_question, user_answer)

            # Update session state and rerun to display the next question
            st.session_state.current_question_index += 1
            st.rerun()
    else:
        # Display interview completion and overall feedback if all questions have been answered
        display_interview_completion(pipeline)

def display_user_info_prompt():
    st.chat_message("assistant").markdown(
        "For the Technical interview, please provide the following information:"
        "\n1. **Job Position** (e.g., Software Engineer, Data Scientist)"
        "\n2. **Question Type** (Multiple Choice or Open-ended)"
    )

    # Collect job position
    job_position = st.chat_input("Enter Job Position")
    if job_position:
        st.session_state.job_position = job_position

    # Display prompt for question type
    question_type = st.radio("Select Question Type", ['Multiple Choice', 'Open-ended'], index=None)
    if question_type:
        st.session_state.question_type = question_type

    # Only proceed if both job position and question type are provided
    if 'job_position' in st.session_state and 'question_type' in st.session_state:
        st.session_state.user_info_collected = True
        st.chat_message("user").markdown(
            f"The job position is **{st.session_state.job_position}** and the question type is **{st.session_state.question_type}**."
        )
        return True
    else:
        st.chat_message("assistant").markdown(
            "Please provide both a valid Job Position and Question Type to proceed."
        )
        return False


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

    with st.expander("Feedback"):
        st.chat_message("assistant").write(feedback)
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
