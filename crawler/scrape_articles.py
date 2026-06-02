import requests
from bs4 import BeautifulSoup

url = "https://portalug.resourceplusonline.com/Home/Detail/how-to-assign-organization-hod-(head-of-department)"

html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

# -------- TITLE --------
print("TITLE:")
print(soup.title.get_text(strip=True))

# -------- CATEGORY --------
category = ""

for link in soup.find_all("a", href=True):
    href = link["href"]

    if "/Home/Categories/" in href:
        category = link.get_text(strip=True)
        break

print("\nCATEGORY:")
print(category)

# -------- VIDEO --------
video_url = None

for link in soup.find_all("a", href=True):
    text = link.get_text(" ", strip=True).lower()

    if "video" in text:
        video_url = link["href"]
        break

print("\nVIDEO URL:")
print(video_url)

# -------- CONTENT --------
article_div = soup.find("div", id="articleContent")

if article_div:
    content = article_div.get_text("\n", strip=True)

    print("\nCONTENT:")
    print(content[:1000])  # first 1000 chars only