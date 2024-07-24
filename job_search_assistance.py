from g4f.client import Client
import g4f
import streamlit as st

# Initialize the client
def generate_text(prompt):
    client = Client()
    response = client.chat.completions.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def run_job_search_assistance():
    st.title('Job Search Assistance')
    st.write("Get tips and advice to enhance your job search.")
    if st.button("Get Job Search Tips"):
        tips_prompt = "Provide some tips for job searching."
        job_search_tips = generate_text(tips_prompt)
        st.markdown(job_search_tips)
