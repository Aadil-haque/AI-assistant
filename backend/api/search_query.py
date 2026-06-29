from groq import Groq
import os

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_search_query(question, history=None):
    if history is None:
        history = []

    conversation = ""

    for item in history[-6:]:
        conversation += f'{item["sender"]}: {item["text"]}\n'

    prompt = f"""
You rewrite search queries for a ResourcePlus knowledge base.

Conversation:
{conversation}

Current Question:
{question}

Your task:

Rewrite the current question into the BEST standalone search query.

Rules:

- Resolve references like:
  - he
  - she
  - him
  - her
  - it
  - this
  - that
  - they
  - them

- If the question is already complete,
  return it unchanged.

- Do NOT answer the question.

- Return ONLY the rewritten search query.

Examples

Conversation:
user: What is HOD?
assistant: ...

Question:
How do I appoint him?

Output:
How to appoint Head of Department (HOD)

Conversation:
user: How to apply leave?
assistant: ...

Question:
Where do I upload it?

Output:
Where to upload documents for leave application

Return ONLY the rewritten query.
"""

    try:

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

        query = response.choices[0].message.content.strip()

        print("\n=========== SEARCH QUERY ===========")
        print(query)
        print("====================================\n")

        return query

    except Exception as e:

        print("Search rewrite error:", e)

        return question