import chromadb
import os
from dotenv import load_dotenv
#import google.generativeai as genai
from groq import Groq
from backend.api.search_query import build_search_query
from backend.api.prompt_builder import build_prompt
from backend.api.history_selector import select_relevant_history
from backend.database.chat_history import (
    save_message,
    get_history
)
from backend.api.title_generator import generate_title

load_dotenv()
#----------------------------------------------
# # Gemini
# genai.configure(
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# model = genai.GenerativeModel(
#     "gemini-2.5-flash"
# )
#----------------------------------------------

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ChromaDB
chroma_client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)

collection = chroma_client.get_collection(
    "resourceplus"
)

# Session Cache
session_cache = {}


def ask_resourceplus(question, history=[],session_id="default"):

    print("=" * 50)
    print("SESSION:", session_id)
    print("=" * 50)

    if session_id not in session_cache:

        session_cache[session_id] = {
            "last_context": "",
            "last_sources": [],
            "last_question": ""
        }
    
    context_cache = session_cache[session_id]
    
    history = get_history(session_id)
    

    selected_history = select_relevant_history(
        question,
        history
    )

    print("\nQUESTION:", question)
    print("\n===== HISTORY DEBUG =====")
    print(type(selected_history))
    print(selected_history)

    if selected_history:
        print(type(selected_history[0]))

    print("=========================\n")

    search_query = build_search_query(
        question,
        selected_history
    )

    print("SEARCH QUERY:", search_query)


    context = ""
    sources = []  

 
    print("USING VECTOR SEARCH")

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

    best_distance = results["distances"][0][0]
    print("BEST DISTANCE:", best_distance)
    # Skip extremely unrelated searches
    MAX_DISTANCE = 1.85

    if best_distance > MAX_DISTANCE:
        return {
            "answer": "This question is outside the ResourcePlus knowledge domain."
        }


    for i in range(len(results["documents"][0])):

        print(
            f"DISTANCE: {results['distances'][0][i]:.4f}",
            "| SOURCE:",
            results["metadatas"][0][i]["title"]
        )

        distance = results["distances"][0][i]

        if distance > best_distance + 0.20:
            continue

        context += (
            results["documents"][0][i]
            + "\n\n"
        )

        sources.append(
            results["metadatas"][0][i]["title"]
        )

    print("\nUsed Sources:")

    for source in sources:
        print(source)



    # Save Context To Cache

    context_cache["last_context"] = context
    context_cache["last_sources"] = sources
    context_cache["last_question"] = question

    # =====================================
    # Conversation History
    # =====================================

    conversation_context =selected_history


    # =====================================
    # Prompt
    # =====================================

    prompt = build_prompt(
        question=question,
        context=context,
        conversation_context=conversation_context
    )


    print("\n========== CONTEXT ==========")

    
    print(context)

    print("=============================\n")

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

        answer = response.choices[0].message.content.strip()
        history = get_history(session_id)

        title = None

        if len(history) == 0:
            title = generate_title(question)
     
    except Exception as e:

        print("Error:", e)

        

        answer = (
            "AI service is temporarily unavailable. "
            "Please try again later."
        )
    
    save_message(
        session_id=session_id,
        sender="user",
        text=question,
        title=title
    )
    save_message(
        session_id=session_id,
        sender="assistant",
        text=answer
    )

    return {
        "answer": answer,
        "sources": sources 
    }