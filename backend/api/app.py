# backend/api/app.py
import chromadb
from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.rag_service import ask_resourceplus
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from backend.database.chat_history import (
    save_message,
    get_history,
    get_conversations,
    get_conversation,
)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "ResourcePlus AI Assistant Running"
    }

#connect ChromeDB
client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)

collection = client.get_collection(
    "resourceplus"
)
#create search funtion
def search_articles(question):

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    return results

#test endpoint
@app.get("/search")
def search(q: str):

    results = search_articles(q)

    articles = []

    for item in results["metadatas"][0]:

        articles.append({
            "title": item["title"],
            "category": item["category"],
            "url": item["url"]
        })

    return articles

class Question(BaseModel):
    question: str
    history: List = []
    session_id: str = "default"

@app.post("/ask")
def ask(data: Question):

    result = ask_resourceplus(
        data.question,
        data.history,
        data.session_id
    )

    return result

@app.get("/conversations")
def conversations():
    return get_conversations()


@app.get("/conversation/{session_id}")
def conversation(session_id: str):
    return get_conversation(session_id)