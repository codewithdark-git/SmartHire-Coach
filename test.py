import g4f
from g4f.client import Client
import json
import sqlite3

def test_client(prompt):
    client = Client()
    response = client.chat.completions.create(
        model=g4f.models.gpt_35_turbo,
        messages=[{"role": "user", "content": prompt}],
        provider='DDG'
    )
    response = response.choices[0].message.content
    return response

response_bot = test_client(
    """ 
        You are a skilled interviewer specializing in {python developer}. Generate a list of 10 technical interview 
        questions related to {python developer}. The questions should include a mix of 
        conceptual questions and coding problems. For each question, provide the question text, a list of 4 answer choices, 
        and indicate the correct answer. Format your response as a JSON array of objects. Each object should contain the 
        keys 'question', 'choices', and 'correct_answer'.

        Example format:
        [
            {
                "question": "What is the time complexity of binary search?",
                "choices": ["O(n)", "O(log n)", "O(n log n)", "O(n^2)"],
                "correct_answer": "O(log n)"
            },
            {
                "question": "Which data structure uses the LIFO principle?",
                "choices": ["Queue", "Stack", "Linked List", "Graph"],
                "correct_answer": "Stack"
            }
        ]

        Please generate the questions in a similar format.
        """)



