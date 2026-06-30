from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_title(question):

    prompt = f"""
Generate a short chat title.

Question:
{question}

Rules:
- Maximum 5 words
- No markdown
- No quotes
- No punctuation at the end
- Return only the title

Examples

How do I apply for leave?
Leave Application

What is HOD?
Head of Department

How to assign department head?
Assign Department Head
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()