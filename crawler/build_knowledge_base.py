import json
import time
import requests
from bs4 import BeautifulSoup

# Load URLs
with open("crawler/data/article_urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

articles = []

for index, url in enumerate(urls, start=1):

    try:
        print(f"[{index}/{len(urls)}] Scraping: {url}")

        response = requests.get(url, timeout=20)

        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title = soup.title.get_text(strip=True)
        #Article ID
        article_id = ""

        h2 = soup.find("h2")

        if h2:
            span = h2.find("span",class_="small pull-right")

            if span:
                article_id = span.get_text(strip=True)

        print(article_id)

        # Category
        category = ""

        for link in soup.find_all("a", href=True):
            if "/Home/Categories/" in link["href"]:
                category = link.get_text(strip=True)
                break
        
        #Tags
        tags = []

        for text in soup.stripped_strings:

            if "~" in text:

                tags = [tag.strip() for tag in text.split("~")]

                break

        print(tags)
      

        # Content
        article_div = soup.find("div", id="articleContent")

        content = ""

        if article_div:
            content = article_div.get_text("\n", strip=True)

        # Video URL
        video_url = None

        for link in soup.find_all("a", href=True):
            text = link.get_text(" ", strip=True).lower()

            if "video" in text:
                video_url = link["href"]
                break

        article = {
            "title": title,
            "Article_ID":article_id,
            "category": category,
            "Tags":tags,
            "url": url,
            "content": content,
            "video_url": video_url
        }

        articles.append(article)

        time.sleep(0.5)

    except Exception as e:
        print(f"Failed: {url}")
        print(e)

# Save output
with open(
    "crawler/data/knowledge_base.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        articles,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"\nSaved {len(articles)} articles")