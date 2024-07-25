from g4f.client import Client
import g4f

# Initialize the client
def generate_text(prompt):
    client = Client()
    response = client.chat.completions.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

