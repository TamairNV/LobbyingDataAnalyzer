import os

import requests
from donations import get_pac_distributions
from main import getAllBill
import dotenv
dotenv.load_dotenv()

PROPUBLICA_API_KEY = os.environ.get("PROPUBLICA_API_KEY")

bills= getAllBill()


CONGRESS_NO = "118"
AMAZON_PAC_ID = "C00360354"
# Your Amazon Data (Paste your list or use the variable from previous step)
# Format: (Amount, Committee Name, Recipient Name if available)

donations = get_pac_distributions(AMAZON_PAC_ID)

def get_bill_cosponsors(bill_slug, congress):
    """
    Fetches the list of politicians sponsoring a specific bill.
    """
    url = f"https://api.propublica.org/congress/v1/{congress}/bills/{bill_slug}/cosponsors.json"
    headers = {'X-API-Key': PROPUBLICA_API_KEY}

    response = requests.get(url, headers=headers)
    data = response.json()

    sponsors = []
    if 'results' in data and data['results']:
        # Add the main sponsor
        sponsors.append(data['results'][0]['sponsor_name'])
        # Add all cosponsors
        for p in data['results'][0]['cosponsors']:
            sponsors.append(p['name'])

    return sponsors


def check_influence(donations, bill_sponsors):
    print(f"Checking {len(bill_sponsors)} sponsors of the bill...\n")

    matches = []

    for amount, committee_name in donations:
        # Simple Logic: Check if any sponsor's last name is in the Committee Name
        # e.g., does "Horsford" appear in "NEVADANS FOR STEVEN HORSFORD"?

        match_found = False
        for sponsor in bill_sponsors:
            # Clean up name: "Horsford, Steven" -> "Horsford"
            last_name = sponsor.split(',')[0]

            if last_name.upper() in committee_name.upper():
                matches.append(
                    f"[MATCH] Amazon gave ${amount:,} to {last_name} ('{committee_name}'), who Co-Sponsored the bill.")
                match_found = True
                break  # Stop checking other sponsors for this donation

        if not match_found:
            # Handle tricky Leadership PACs (Dark Money)
            if "PAC" in committee_name and not match_found:
                print(f"[UNK]  ${amount:,} to '{committee_name}' (Leadership PAC - Hard to link automatically)")
            else:
                print(f"[---]  ${amount:,} to '{committee_name}' (No link to bill found)")

    print("\n" + "=" * 40 + "\n")
    for m in matches:
        print(m)


# --- Execute ---
for b in bills:
    sponsors = get_bill_cosponsors(b, CONGRESS_NO)
    check_influence(donations, sponsors)