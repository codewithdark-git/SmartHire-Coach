import streamlit as st
from utils.real_time_pipeline import RealTimePipeline
from utils.helper import (
    extract_skills,
    summarize_experience,
    extract_education,
    extract_text_from_docx,
    extract_text_from_pdf,
    analyze_resume,
    generate_prompt,
    calculate_resume_score,
    parse_response
)
import nltk


# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

pipeline = RealTimePipeline()

def main():
    st.set_page_config(page_title="Advanced Resume Analyzer", page_icon="📄", layout="wide")

    st.title("📄 Advanced Resume Analyzer")
    st.write("Upload your resume and get personalized insights and recommendations!")

    uploaded_file = st.file_uploader("📎 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file is not None:
        progress_bar = st.progress(0)
        progress_text = st.empty()

        progress_text.text("Analyzing your resume... This may take a moment.")
        try:
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                st.error("❌ Unsupported file format. Please upload a PDF or DOCX file.")
                return

            progress_bar.progress(25)
            progress_text.text("Extracting information from the resume...")
            skills, experience_summary, education = analyze_resume(resume_text)
            progress_bar.progress(50)

            progress_text.text("Generating insights and recommendations...")
            prompt = generate_prompt(skills, experience_summary, education)

            try:
                response = pipeline.generate_text(prompt)
                improvements, job_suggestions = parse_response(response)
            except Exception as e:
                st.error(f"❌ Error in generating improvements and job suggestions: {str(e)}")
                improvements = ["Unable to generate improvements at this time."]
                job_suggestions = ["Unable to generate job suggestions at this time."]

            resume_score = calculate_resume_score(resume_text, skills, education)
            progress_bar.progress(75)

            progress_text.text("Finalizing the analysis...")
            st.success("✅ Resume analysis complete!")

            st.subheader("📊 Resume Score")
            st.progress(resume_score / 100)
            st.write(f"Your resume scored {resume_score}/100")

            st.subheader("🚀 Improvement Suggestions")
            for i, imp in enumerate(improvements, 1):
                st.write(f"{i}. {imp}")

            st.subheader("🔍 Extracted Skills")
            skills = f""" {resume_text} this is resume text and we want to Extract skills from the resume using the following pattern (case-insensitive):
                        proficient in " or " experienced with " or " skilled in " or " knowledge of " followed
                        by a comma-separated list of skills. Example: 'Experienced with Python, Java, SQL,
                        JavaScript, React, Node.js, and Machine Learning.' """
            res = pipeline.generate_text(skills)
            st.write(res)

            st.subheader("💼 Potential Job Matches")
            for i, job in enumerate(job_suggestions, 1):
                st.write(f"{i}. {job}")

            st.subheader("📚 Education")
            edu_prompt = f"""Summarize the education details from: {education}
            Format the response as: "Degree, Institution, Years of Study"
            Example: "Bachelor of Science in Computer Science, University of California, Los Angeles, 2015-2020"
            If specific details are missing, use placeholder text."""
            edu_response = pipeline.generate_text(edu_prompt)
            st.write(edu_response)

            st.subheader("💡 Experience Summary")
            exp_prompt = f"""Summarize the work experience from: {experience_summary}
            Format the response as: "Job Title, Company Name, Location, Years of Experience, Brief Description"
            Example: "Software Engineer, Google, Mountain View, 3 years, Developed web applications using Python and Django"
            If specific details are missing, use placeholder text. Limit to 2-3 most recent or relevant positions."""
            exp_response = pipeline.generate_text(exp_prompt)
            st.write(exp_response)

            progress_bar.progress(100)
            progress_text.text("Analysis complete.")

        except Exception as e:
            st.error(f"❌ An error occurred while processing the resume: {str(e)}")
            st.write("Please try uploading your resume again or contact support if the issue persists.")


if __name__ == "__main__":
    main()
