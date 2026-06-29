from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def select_relevant_history(question, history):

    if not history:
        return []

    conversation = ""

    for item in history:
        conversation += (
            f"{item['sender']}: {item['text']}\n"
        )

    prompt = f"""
You are selecting conversation history.

Conversation:

{conversation}

Current Question:

{question}

Return ONLY the conversation messages needed to answer the current question.

If none are needed return:

NONE
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

    answer = response.choices[0].message.content.strip()

    if answer.upper() == "NONE":
        return []

    return answer