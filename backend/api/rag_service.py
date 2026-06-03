import chromadb
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Gemini configuration
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ChromaDB
client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)

collection = client.get_collection(
    "resourceplus"
)


def ask_resourceplus(question):

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = ""

    sources = []

    for i in range(len(results["documents"][0])):

        context += (
            results["documents"][0][i]
            + "\n\n"
        )

        sources.append(
            results["metadatas"][0][i]["title"]
        )

    prompt = f"""
You are a ResourcePlus knowledge-base assistant.

Answer ONLY using the supplied context.

If the answer is not found in the context,
say:
"I could not find that information in the knowledge base."

CONTEXT:

{context}

QUESTION:

{question}
"""

    response = model.generate_content(
        prompt
    )

    return {
        "answer": response.text,
        "sources": sources
    }