import streamlit as st
import re
from ulits.helper import extract_text_from_pdf, extract_text_from_docx, preprocess_text
from ulits.response import generate_text


st.header("Resume Review")
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX):")

if uploaded_file is not None:
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        resume_text = None

    if resume_text:
        st.write("Parsed Resume Data:", resume_text)

        resume_text = preprocess_text(resume_text)
        st.write("Preprocessed Resume Data:", resume_text)

        review_prompt = f"Provide suggestions to improve this resume: {resume_text}"
        resume_review = generate_text(review_prompt)
        st.text_area("Resume Review", resume_review)

        resume_text = preprocess_text(resume_text)
        keywords = re.findall(r'\b\w*[a-zA-Z]+\w*\b', resume_text)
        st.write("Extracted Keywords:", ', '.join(keywords))

        keyword_prompt = f"Provide suggestions to improve the resume based on these keywords: {', '.join(keywords)}"
        keyword_review = generate_text(keyword_prompt)
        st.text_area(keyword_review)