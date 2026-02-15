import os

import requests
import dotenv
dotenv.load_dotenv()


FEC_API_KEY = os.environ.get("GOV_API")

def find_pac_id(company_name):
    print(f"Searching for PACs related to '{company_name}'...")

    url = "https://api.open.fec.gov/v1/committees/"

    params = {
        'api_key': FEC_API_KEY,
        'q': company_name,  # The text search (e.g., "Amazon", "Google")
        'sort': 'name',
        'per_page': 20,
        'committee_type': ['N', 'Q'],  # N=Nonqualified PAC, Q=Qualified PAC (Filters out candidates)
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    data = response.json()

    # Filter and Display Results
    found_any = False

    if 'results' in data:
        print(f"{'ID':<10} | {'Committee Name'}")
        print("-" * 60)

        for pac in data['results']:
            # We only want Lobbyist/Registrant PACs (Designation B) or unauthorized (U)
            # This filters out random candidates who might have "Amazon" in their address
            if pac['designation'] in ['B', 'U', 'D']:
                print(f"{pac['committee_id']:<10} | {pac['name']}")

                found_any = True
                return pac['committee_id']

    if not found_any:

        print("No obvious PACs found. Try a broader search term.")
        return False


