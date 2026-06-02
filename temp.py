import json

with open(
    "crawler/data/knowledge_base.json",
    "r",
    encoding="utf-8"
) as f:
    articles = json.load(f)

bad_count = 0

for article in articles:

    title = article.get("title", "")

    if "_Layout.cshtml" in title:
        bad_count += 1

        print("\nBAD ARTICLE")
        print("URL:", article.get("url"))
        print("TITLE:", title)

print("\nTotal bad articles:", bad_count)