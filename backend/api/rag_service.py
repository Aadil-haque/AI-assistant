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

def build_search_query(question, history=[]):

    q = question.lower()

    pronouns = [
        "he",
        "she",
        "him",
        "her",
        "it",
        "they",
        "them"
    ]

    if any(word in q for word in pronouns):

        last_topic = ""

        for item in reversed(history):

            if item["sender"] != "user":
                continue

            text = item["text"]

            if text.lower() == question.lower():
                continue

            last_topic = text
            break

        if last_topic:
            return f"{last_topic} {question}"

    return question

def ask_resourceplus(question,history=[]):
    
    print("\nQUESTION:", question)
    
    search_query = build_search_query(
        question,
        history
    )

    print("SEARCH QUERY:", search_query)

    results = collection.query(
        query_texts=[search_query],
        n_results=8
    )
    print(results["distances"])
    print(
        "\nTOP DOCUMENTS:",
        len(results["documents"][0])
    )

   
    if not results["documents"][0]:
        return {
            "answer":
            "I could not find that information in the knowledge base.",
            "sources": []
        }
   
    context = ""
    conversation_context = ""

    sources = []

    best_distance = results["distances"][0][0]

    for i in range(len(results["documents"][0])):
        print(
            f"DISTANCE: {results['distances'][0][i]:.4f}",
            "| SOURCE:",
            results["metadatas"][0][i]["title"]
        )

        distance = results["distances"][0][i]

        if distance > best_distance + 0.25:
            continue

        context += results["documents"][0][i] + "\n\n"

        sources.append(
            results["metadatas"][0][i]["title"]
        )
    print("\nused source:")
    for source in sources:
        print(source)

    for item in history[-10:]:

        conversation_context += (
            f"{item['sender']}: "
            f"{item['text']}\n"
        )

    prompt = f"""
    You are the official ResourcePlus AI Assistant.

    Use the retrieved knowledge as the primary source of truth.

    You may use the previous conversation to understand references such as:

    - he
    - she
    - him
    - her
    - it
    - they
    - this
    - that

    If the current question refers to something discussed earlier,
    use the conversation history to determine the subject.

    Answer ONLY using the retrieved knowledge.

    

    If the context contains related information    
    provide the closest helpful answer .

    Only say
    "I could not find that information in the knowledge base."
    when the context is completely unrelated.

    ----------------------------------

    RETRIEVED KNOWLEDGE:

    {context}

    ----------------------------------

    PREVIOUS CONVERSATION:

    {conversation_context}

    ----------------------------------

    CURRENT QUESTION:

    {question}

    ----------------------------------

    Formatting Rules:

    - Use headings.
    - Use bullet points.
    - Use numbered steps for procedures.
    - Highlight important terms in markdown bold.
    - Keep answers concise.

    """
    print("\n========== CONTEXT ==========")
    print(context)
    print("=============================\n")

    try:

        response = model.generate_content(
            prompt
        )

        answer = response.text

    except Exception as e:

        print("Gemini Error:", e)

        answer = (
            "AI service is temporarily unavailable. "
            "Please try again later."
        )

    return {
        "answer": answer,
        "sources": []
    }