import json
import os

import requests
import pdfplumber

names = []
bills = []
total = 0
with open("Documents/Amazon LLC.json", "r") as f:
    data = json.load(f)
    for item in data:

        if type(data[item]) == dict:
            d = data[item]
            if d['bill']['committee_name'] not in bills:
                bills.append( d['bill']['committee_name'])
            else:
                continue
            for name in d["paidMembers"]:
                n = name['member_name']

                total += name['amount']
                if n not in names:
                    names.append(n)

import requests
import pdfplumber
import io

# The URL you found (that was giving you a 403)
url = "https://s2.q4cdn.com/299287126/files/doc_downloads/2024/political-engagement-statement.pdf"
# Note: You might need to dynamically find this URL by scraping the 'ir.aboutamazon.com' page first.


import pdfplumber
import re

# Name of your local file
import requests
import json
import dotenv
dotenv.load_dotenv()

PROPUBLICA_API_KEY = os.environ.get("PROPUBLICA_API_KEY")
# You found these names in the Amazon PDF
TARGETS = ["NetChoice", "Business Roundtable"]

import pdfplumber
import re


def extract_amazon_proxies(pdf_path):
    proxies = []

    with pdfplumber.open(pdf_path) as pdf:
        print(f"Scanning {len(pdf.pages)} pages for Trade Association data...")

        for page in pdf.pages:
            text = page.extract_text()

            for target in TARGETS:
                if target in text:
                    print(f"Found Trade Association data for {target}")
    return proxies


# Usage
file_path = "amazon_report.pdf"
proxy_data = extract_amazon_proxies(file_path)
print(proxy_data)
# Run the search
