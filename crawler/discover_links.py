import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

BASE_URL = "https://portalug.resourceplusonline.com/"

response = requests.get(BASE_URL)

print("Status:",response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

article_urls = set()

for links in soup.find_all("a", href=True):
    href = links["href"]

    if "/Home/Detail" in href:
        full_url =urljoin(BASE_URL, href)
        article_urls.add(full_url)

print(f"Found {len(article_urls)} Articles")

with open ("data/article_urls.json", "w") as f :
    json.dump(list(article_urls), f, indent=4)

print("Saved article URLs")