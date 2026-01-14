

API_KEY ='pub_9ca6474a0daa4c659e28731d1995b4bc'
import requests

BASE_URL = "https://newsdata.io/api/1/news"

query = 'Amazon AND "Increasing Access to Biosimilars Act"'
params = {
    'apikey': API_KEY,
    'language': 'en',
    'country': 'us',
    'q' : query
}

response = requests.get(BASE_URL, params=params)
data = response.json()

if response.status_code == 200:
    print(f"Found {data.get('totalResults')} articles:")
    for article in data.get('results', []):
        print(f"- {article['title']} ({article['pubDate']})")
else:
    print("Error:", data)