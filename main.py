import requests
import json
from searchTest import *
# 1. Define the correct parameters
url = "https://lda.senate.gov/api/v1/filings/"
params = {
    "client_name": "Amazon LLC",
    "filing_year": "2024",  # FORCE it to look at 2024

}
from regex import extract_bill_codes

def getAllBill():
    response = requests.get(url, params=params)
    data = response.json()

    json_str = json.dumps(data, indent=4)
    with open("sample.json", "w") as f:
        f.write(json_str)
    codes = []
    # 2. Loop through results
    for filing in data['results']:
        if filing.get('filing_type') == None:
            continue
        if filing['filing_type'] != "Q1":
            continue
        # Only look at the filing if it has expenses listed
        if filing['expenses']:
            print(f"📅 Period: {filing['filing_year']} {filing['filing_period']}")
            print(f"💰 Expenses: ${filing['expenses']}")

            # 3. Extract Bills from the 'description' field
            # print("📜 Specific Issues:")

            for activity in filing['lobbying_activities']:
                if activity['description']:
                    # This prints the text where the bill numbers are hiding
                    print(f"   - {activity['general_issue_code']}: {activity['description']}...")

                    codes += extract_bill_codes(activity['description'])

                if activity.get('lobbyists') != None:
                    for p in activity['lobbyists']:
                        person = p['lobbyist']

                        # print(f"{person['first_name']} {person['last_name']}")
            print("-" * 40)
    newCodes = []
    for code in codes:
        newCodes.append(str(code).replace(".",'').replace(" ",''))



    return newCodes


getAllBill()