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

    SmartHire Coach is your personal AI-powered career assistant, designed to assist you with resume analysis, job matching, and interview preparation. Our mission is to empower job seekers and professionals with the tools they need to succeed in their career journeys. By leveraging advanced AI and natural language processing, SmartHire Coach provides personalized insights and actionable recommendations tailored to your unique profile.
    """)

    st.markdown("""
    ### Instructions on How to Use the App 📄

    1. **Upload Your Resume**: Click on the "Upload your resume" button and select your resume file (PDF or DOCX).
    2. **Analyze Your Resume**: Once the file is uploaded, the app will automatically analyze your resume and provide insights on your skills, experience, and education.
    3. **View Recommendations**: Check the suggested improvements and potential job matches based on your resume analysis.
    4. **Improve Your Resume**: Follow the recommendations to enhance your resume and boost your chances of landing your desired job.
    5. **Prepare for Interviews**: Use the job suggestions and feedback to prepare for your upcoming interviews.
    """)

    st.markdown("""
    ### More About SmartHire Coach 🚀

    - **AI-Powered Analysis**: Leverages state-of-the-art natural language processing to analyze resumes and extract crucial information.
    - **Personalized Recommendations**: Offers tailored advice to refine your resume and identify fitting job opportunities.
    - **Interview Preparation**: Assists you in preparing for interviews by providing relevant questions and feedback.
    - **User-Friendly Interface**: Designed for ease of use, allowing you to navigate through the app effortlessly.
    - **Continuous Updates**: We are committed to continuously improving the app with new features and enhancements.

    ### About the Developer 👨‍💻

    SmartHire Coach is developed by a passionate team of AI enthusiasts and career advisors dedicated to helping individuals succeed in their professional endeavors. With a background in machine learning and career consulting, the team brings together expertise from various fields to create a comprehensive and user-friendly app. We are constantly working on new features and improvements to ensure the best possible experience for our users. Feel free to reach out with any feedback or suggestions!

    **Contact Us:** If you have any questions or need support, please contact us at [codewithdark90@gmail.com](mailto:codewithdark90@gmail.com).
    **More Information:** Visit our [website](https://link.tree/codewithdark) or follow us on [LinkedIn](https://www.linkedin.com/in/codewithdark/) to learn more about our mission and team.
    """)

    st.markdown("""
    ### Get Started Now! 🏁

    Ready to elevate your career? Upload your resume and let SmartHire Coach guide you through your job search journey!
    """)

    st.page_link('pages/interview.py', label='Prepare for interviews', icon='📑')
    st.page_link('pages/Resume Analyzer.py', label='Upload your resume', icon='🪧')

if __name__ == "__main__":
    main()
