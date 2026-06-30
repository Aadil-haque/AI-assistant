from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def select_relevant_history(question, history):

    if not history:
        return []

    numbered_history = ""

    for i, item in enumerate(history):

        numbered_history += (
            f"{i}. "
            f"{item['sender']}: "
            f"{item['text']}\n"
        )

    prompt = f"""
You are selecting conversation history for a chatbot.

Conversation:

{numbered_history}

Current Question:

{question}

Return ONLY a JSON array of message indexes.

Examples:

[]

[0]

[2,3]

[1,2,5]

Rules:

- Return only indexes.
- No explanation.
- No markdown.
- No text.
- If nothing is relevant return [].
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

    print("\nLLM HISTORY SELECTION:")
    print(answer)

    try:

        indexes = json.loads(answer)

        if not isinstance(indexes, list):
            return []

        selected = []

        selected_indexes = set()

        for i in indexes:

            if not isinstance(i, int):
                continue

            if i < 0 or i >= len(history):
                continue

            selected_indexes.add(i)

            # include previous user message
            if (
                history[i]["sender"] == "assistant"
                and i > 0
                and history[i-1]["sender"] == "user"
            ):
                selected_indexes.add(i-1)

        selected = [
            history[i]
            for i in sorted(selected_indexes)
        ]

        return selected

    except Exception:

        print("Failed to parse history selection.")
        return []