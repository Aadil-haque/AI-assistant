# backend/api/app.py
import chromadb
from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.rag_service import ask_resourceplus


app = FastAPI()

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

@app.post("/ask")
def ask(data: Question):

    result = ask_resourceplus(
        data.question
    )

    return result
