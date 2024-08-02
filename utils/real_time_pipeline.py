import g4f
import g4f.Provider
from g4f.client import Client
import sqlite3
import json
import io


def generate_response(prompt):
    try:
        client = Client()
        response = client.chat.completions.create(
            model=g4f.models.gpt_4o,
            messages=[{"role": "user", "content": prompt}],
            # provider=g4f.Provider.Pizzagpt
        )
        response_text = response.choices[0].message.content
        # print("Generated Response:", response_text)  # Debug print
        return response_text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def generate_prompt(job_position):
    return f"""You are a skilled interviewer specializing in {job_position}. Generate a list of 50 technical interview 
    questions related to {job_position}. The questions should include a mix of conceptual questions and coding problems. 
    For each question, provide the question text, a list of 4 answer choices, and indicate the correct answer. 
    Format your response as
    [
        {{
            "question": "What is the time complexity of binary search?",
            "choices": ["O(n)", "O(log n)", "O(n log n)", "O(n^2)"],
            "correct_answer": "O(log n)"
        }},
        ...
    ]
    """

def create_db():
    conn = sqlite3.connect('chatbot_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, tag TEXT)''')
    conn.commit()
    return conn

def insert_question(conn, question, tag):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (question, tag) VALUES (?, ?)", (question, tag,))
    conn.commit()


def fetch_questions_from_db(conn, tag):
    """Fetches all questions from the database and returns them as a list of dictionaries."""
    cursor = conn.cursor()
    cursor.execute("SELECT question FROM questions WHERE tag=? """)
    rows = cursor.fetchall()
    all_questions = []
    for row in rows:
        try:
            questions_list = json.loads(row[0])  # Parse JSON string to get a list of questions
            all_questions.extend(questions_list)  # Add all questions to the list
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    return all_questions

def display_questions(questions):
    """Displays questions, choices, and correct answers."""
    for question_dict in questions:
        question_text = question_dict.get("question", "No question available")
        choices = question_dict.get("choices", [])
        correct_answer = question_dict.get("correct_answer", "No correct answer available")
        
        print(f"Question: {question_text}")
        print("Choices:")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        print(f"Correct Answer: {correct_answer}")
        print("---")

def main():
    tag = 'python developer'
    prompt = generate_prompt(tag)
    response = generate_response(prompt)


    if not response:
        print("Received an empty response.")
        return
    
    # Connect to the SQLite database and insert the generated response into the database
    conn = create_db()

    insert_question(conn, response, tag)
    
    conn = sqlite3.connect('chatbot_db.sqlite')
    
    # Fetch questions from the database
    questions = fetch_questions_from_db(conn, tag)
    
    # Display each question with its choices and correct answer
    display_questions(questions)

    conn.close()

if __name__ == "__main__":
    main()
