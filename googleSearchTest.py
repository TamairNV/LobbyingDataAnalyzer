
API_KEY = "AIzaSyCPijxCYicDBCvcPxXgL8sRUqyO61_5v5U"
CSE_ID = "e5f1c0091c48a4108"


from googleapiclient.discovery import build
from newspaper import Article
import time


def search_google(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CSE_ID, num=5).execute()
    return res.get('items', [])


import trafilatura

# Replace the get_article_text function above with this:
def get_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Could not retrieve article: {e}"
# --- Main Execution ---
search_query = '"American Innovation and Jobs Act" AND Amazon AND (lobby OR lobbying OR opposed OR supported)'

print(f"Searching for: {search_query}...\n")
results = search_google(search_query)


info = {}

for i, item in enumerate(results, start=1):
    title = item['title']
    link = item['link']
    info[title] = {}

    print(f"--- Article {i} ---")
    print(f"Title: {title}")
    print(f"Link:  {link}")

    # Extract the full text
    print("Downloading text...", end=" ")
    full_text = str(get_article_text(link))
    print(full_text)

    # Print the first 500 characters of the text to keep output clean
    print("Done!\n")
    if full_text != None:
        info[title]['fullText'] = full_text
        print(f"Snippet: {full_text[:500]}...")
        print("\n" + "=" * 50 + "\n")

    # Respect server limits (be nice to the websites)
    time.sleep(1)

print(info)