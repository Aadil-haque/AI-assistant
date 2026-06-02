import chromadb

client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)

collection = client.get_collection("resourceplus")

print("Documents:", collection.count())