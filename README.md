# SmartHire Coach 🎓

## Overview
**SmartHire Coach** is an AI-powered interview preparation app designed to help job seekers practice and refine their interview skills. The app offers both general and technical interview practice, providing users with realistic interview questions and valuable feedback on their answers. Whether you're preparing for a general interview or a technical role, SmartHire Coach is here to guide you through the process and help you succeed.

## Features
- **General and Technical Interviews**: Choose between general and technical interview types, tailored to different job roles and industries.
- **Customizable Settings**: Users can specify job positions and question types (multiple choice or open-ended) for a personalized interview experience.
- **Real-Time Feedback**: Get immediate, constructive feedback on your answers to help you improve your responses.
- **Session Persistence**: Your interview progress is saved, allowing you to review previous questions and answers.
- **Detailed Feedback**: After completing an interview, receive detailed feedback on your performance, including strengths and areas for improvement.
- **Resume Analysis**: Upload your resume to receive a comprehensive analysis, including skill extraction, experience summary, and education details.

## Getting Started
### Prerequisites
To run the app, you will need:
- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- Your preferred LLM integration library (e.g., `g4f`, OpenAI, etc.)
- Your API key (stored in a `.env` file for security)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/codewithdark-git/smarthire-coach.git
   cd smarthire-coach
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with the necessary API keys:
   ```sh
   echo "AI71_API_KEY=your_api_key_here" > .env
   ```
##### *OR*
  Used the G4f library For free used LLM:
   ```sh
   def generate_text(self, prompt):
   pass
   ```

### Running the App
To start the app, run:
```sh
streamlit run main.py
```
The app will be accessible at `http://localhost:8501` by default.

## Usage
1. **Select Interview Type**: Choose between "General" or "Technical" interviews from the sidebar.
2. **Provide Job Position and Question Type**: For technical interviews, specify the job position and select the type of questions (multiple choice or open-ended).
3. **Answer Questions**: Respond to the questions presented by the assistant.
4. **Receive Feedback**: After answering, receive feedback on your response. Continue to the next question or review your detailed feedback at the end of the session.
5. **Resume Analysis**: Upload your resume (PDF or DOCX) and receive insights into your skills, experience, and education. Get suggestions for improvements and potential job roles.

## Contributing
We welcome contributions from the community! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear commit messages.
4. Push your changes to your fork.
5. Create a pull request, describing the changes you made.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Special thanks to the [Streamlit](https://streamlit.io/) team for their awesome open-source project.
- Thanks to all contributors and users who provide feedback and suggestions.

---

For any questions or support, please open an issue on GitHub or contact the project maintainers. Happy interviewing! 🎓