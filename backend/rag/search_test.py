import chromadb

client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)

collection = client.get_collection("resourceplus")

results = collection.query(
    query_texts=[
        "attendance shift assignment"
    ],
    n_results=5
)

for i in range(len(results["ids"][0])):

    print("\n" + "=" * 60)

    print("ID:", results["ids"][0][i])

    print("TITLE:",
          results["metadatas"][0][i]["title"])

    print("CATEGORY:",
          results["metadatas"][0][i]["category"])

    print("DISTANCE:",
          results["distances"][0][i])