import json
import chromadb

client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)

# Delete old collection if it exists
try:
    client.delete_collection("resourceplus")
    print("Old collection deleted")
except:
    print("No existing collection found")


# Create fresh collection
collection = client.create_collection(
    name="resourceplus"
)

with open(
    "crawler/data/knowledge_base.json",
    "r",
    encoding="utf-8"
) as f:

    articles = json.load(f)

print("Loaded:", len(articles))

inserted=0
for article in articles:
    try:
        article_id = str(article.get("Article_ID", "")).strip()

        if not article_id:
            print("Missing ID:")
            print(article.get("title"))
            continue
        
        title = article.get("title", "")
        content = article.get("content", "")
        article_id = str(article.get("Article_ID", "")).strip()

        # Skip bad ASP.NET pages
        if "_Layout.cshtml" in title:
            continue

        # Skip empty IDs
        if not article_id:
            continue

        # Skip empty content
        if not content.strip():
            continue

        collection.add(
            ids=[article_id],
            documents=[content],
            metadatas=[
                {
                    "title": article["title"],
                    "category": article["category"],
                    "url": article["url"]
                }
            ]
        )
        inserted += 1

    except Exception as e:
        print(f"Failed: {article['title']}")
        print(e)
inserted += 1
print(f"\ninserted {inserted} articles")