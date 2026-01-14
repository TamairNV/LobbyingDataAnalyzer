import os

import requests
import json


import dotenv
dotenv.load_dotenv()

API_KEY = os.environ.get("PROPUBLICA_API_KEY")
BASE_URL = "https://api.open.fec.gov/v1"





def get_pac_distributions(committee_id):
    # Endpoint: Schedule B (Disbursements) by the committee
    url = f"{BASE_URL}/schedules/schedule_b/"

    params = {
        "api_key": API_KEY,
        "committee_id": committee_id,
        "two_year_transaction_period": 2024,  # Current cycle
        "per_page": 20,
        "sort": "-disbursement_date"
    }

    response = requests.get(url, params=params).json()
    print(response)
    data = []
    if 'results' in response:
        for item in response['results']:
            # Filter for contributions to committees/candidates

            if item.get('recipient_committee_id'):


                date = item['disbursement_date']
                amount = item['disbursement_amount']
                recipient = item['recipient_name']
                state = item['recipient_state']
                t = (amount,recipient)
                data.append(t)

    return data




