from duckduckgo_search import DDGS




import requests

# 1. PASTE YOUR NEW KEY HERE


API_KEY = "Ya5iCfcRfK8ggOkeeR24j0rVv8CjRHJf0FKANpcB"
def get_bill_data(congress, bill_type, bill_number):

    # 2. THE NEW ENDPOINT
    base_url = "https://api.congress.gov/v3"
    url = f"{base_url}/bill/{congress}/{bill_type}/{bill_number}?api_key={API_KEY}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors

        data = response.json()
        bill = data.get('bill', {})

        # 3. EXTRACT THE MOTIVE CLUES
        print(f"--- {bill_type.upper()} {bill_number} ---")
        print(f"Title: {bill.get('title')}")

        # Subject extraction (sometimes nested)
        policy_area = bill.get('policyArea', {}).get('name', 'N/A')
        print(f"Policy Area (Motive Clue): {policy_area}")

        # Get the latest summary text if available
        # (Note: Summaries are a separate endpoint in V3, but this gives the main topic)

    except Exception as e:
        print(f"Error fetching bill: {e}")


# --- TEST IT ---
# Testing the bills from your Amazon list:

# Cannabis Administration & Opportunity Act (S. 4591 - 117th Congress)
get_bill_data(117, "s", "4591")

# Equality Act (H.R. 5 - 117th Congress)
get_bill_data(117, "hr", "5")