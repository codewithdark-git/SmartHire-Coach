import streamlit as st


def main():
    st.set_page_config(page_title="SmartHire Coach", page_icon="🤖", layout="centered")

    st.markdown("""
    <style> 
        div.stButton > button:first-child { 
            background-color: rgb(204, 49, 49);
            color: white;
        }

        div.stButton > button:first-child:hover {
            background-color: white;
            color: rgb(204, 49, 49);
            border: 2px solid rgb(204, 49, 49);
        } 

        .title {
            text-align: center;
        }

        .instructions {
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    # SmartHire Coach

    ## Welcome to SmartHire Coach! 🤖

    ### Hi there 👋

    SmartHire Coach is your personal AI-powered career assistant, designed to help you with resume analysis, job matching, and interview preparation. Our goal is to provide you with personalized insights and recommendations to enhance your job search process.
    """)

    st.markdown("""
    ### Instructions on How to Use the App 📄

    1. **Upload Your Resume**: Click on the "Upload your resume" button and select your resume file (PDF or DOCX).
    2. **Analyze Your Resume**: Once the file is uploaded, the app will automatically analyze your resume and provide insights on your skills, experience, and education.
    3. **View Recommendations**: Check the suggested improvements and potential job matches based on your resume analysis.
    4. **Improve Your Resume**: Follow the recommendations to improve your resume and increase your chances of landing your desired job.
    5. **Prepare for Interviews**: Use the job suggestions and feedback to prepare for your upcoming interviews.
    """)

    st.markdown("""
    ### More About SmartHire Coach 🚀

    - **AI-Powered Analysis**: Utilizes advanced natural language processing to analyze your resume and extract key information.
    - **Personalized Recommendations**: Provides tailored suggestions to improve your resume and identify suitable job roles.
    - **Interview Preparation**: Helps you prepare for interviews with relevant questions and feedback.
    - **Continuous Improvement**: We constantly update the app with new features and improvements to serve you better.
    """)

    st.markdown("""
    ### Get Started Now! 🏁

    Ready to enhance your career prospects? Upload your resume and let SmartHire Coach assist you in your job search journey!
    """)

    if st.button("Upload your resume"):
        st.write("Upload functionality will be here...")


if __name__ == "__main__":
    main()
