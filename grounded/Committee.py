import json
import os
import time
import re
import requests
from nameparser import HumanName
from rapidfuzz import fuzz

from PAC import find_pac_id
import dotenv
dotenv.load_dotenv()

PROPUBLICA_API_KEY = os.environ.get("PROPUBLICA_API_KEY")
GOV_API = os.environ.get("GOV_API")
headers = {'X-API-Key': PROPUBLICA_API_KEY}
from regex import extract_bill_codes
CYCLE = 2024
class Bill():
    def __init__(self,congress_no,bill_type,bill_num):
        url = f"https://api.congress.gov/v3/bill/{congress_no}/{bill_type}/{bill_num}/committees"
        self.params = {
            'api_key': GOV_API,
            'format': 'json'
        }
        self.congress_no = congress_no
        response = requests.get(url,headers=headers).json()
        self.id = None
        self.bill_type = bill_type
        self.bill_num = bill_num
        if response.get('committees') == None:
            print(f"No Committee for {self.bill_type + self.bill_num}")
            return
        if len(response['committees']) == 0:
            print(f"No Committee for {self.bill_type + self.bill_num}")
            return

        self.committee_name = response['committees'][0]['name']
        self.id = response['committees'][0]['systemCode']
        self.id = self.id[:len(self.id)-2]
        self.chamber = "house"
        if self.bill_type.lower().startswith("s"):
            self.chamber = "senate"

        print(f"{self.bill_type + self.bill_num} {self.committee_name} {self.id}")
        #self.getVotes()

    def getVotes(self):
        url = f"https://api.congress.gov/v3/bill/{self.congress_no}/{self.bill_type}/{self.bill_num}/actions"
        #data = requests.get(url,headers=headers).json()
        #print(data)

    def getJsonItem(self):
        item = {
            "bill_no" : self.bill_num,
            "bill_type" : self.bill_type,
            "chamber" : self.chamber,
            "committee_name" : self.committee_name,
            "committee_id" : self.id
        }
        return item

def get_official_names():
    print("Downloading official name roster...")
    url = "https://unitedstates.github.io/congress-legislators/legislators-current.json"
    data = requests.get(url).json()

    # Create a quick lookup: {'C001113': 'Cortez Masto', 'W000779': 'Wyden'}
    lookup = {}
    for person in data:
        bioguide = person['id']['bioguide']
        last_name = person['name']['last']  # This handles "Cortez Masto" perfectly
        lookup[bioguide] = last_name.upper()

    return lookup

class Committee():

    members = get_official_names()
    committeeMembers = requests.get("https://unitedstates.github.io/congress-legislators/committee-membership-current.json").json()
    def __init__(self,id,chamber,congress_no):
        self.id = id
        self.members = Committee.committeeMembers[id.upper()]

    def getJsonItem(self):
        item = {
            "committee_id" : self.id,
            "members": self.members

        }
        return item



class Lobbying():
    def __init__(self,company):
        url = "https://lda.senate.gov/api/v1/filings/"
        params = {
            "client_name": company,
            "filing_year": "2025",
        }
        self.company = company
        self.logourl = get_company_logo(company)
        self.PACID = find_pac_id(company)
        if not self.PACID:
            print(f"No PAC found for {company}")
            return
        response = requests.get(url, params=params)
        data = response.json()
        codes = []
        print("Getting all lobbied bills")
        for filing in data['results']:
            if filing.get('filing_type') == None:
                continue
            if filing['expenses']:
                #print(f"📅 Period: {filing['filing_year']} {filing['filing_period']}")
                #print(f"💰 Expenses: ${filing['expenses']}")

                for activity in filing['lobbying_activities']:
                    if activity['description']:

                        codes += extract_bill_codes(activity['description'])

        self.newCodes = []
        for code in codes:
            newCode = str(code).replace(".", '').replace(" ", '').lower()
            if newCode in self.newCodes:
                continue
            if code[0].lower() == "s" or code[0].lower() == "h":
                self.newCodes.append(newCode)
        self.donations = self.getDonations()
        self.paidMembers = {
            "Company_Name": self.company,
            "PAC_no": self.PACID,
            "LogoURL": self.logourl,
        }
        i = 1
        print("Getting paid members")

        for code in self.newCodes:

            pm = self.getPaidMembers(code)
            if pm is None:
                continue
            self.paidMembers[code] = {
                "bill": pm[1].getJsonItem(),
                "paidMembers" : pm[0]
            }
            time.sleep(0.2)
            i+=1


        with open(f"Documents/{self.company}.json",'w') as f:
            j = json.dumps(self.paidMembers, indent=4)
            f.write(j)
    def getDonations(self):
        print("Fetching PAC donations...")

        url = "https://api.open.fec.gov/v1/schedules/schedule_b/"

        all_donations = []

        params = {
            'api_key': GOV_API,
            'committee_id': self.PACID,
            'two_year_transaction_period': CYCLE,
            'per_page': 100,
            'sort': '-disbursement_date',  # Explicitly sort by date (Newest first)
        }

        while True:
            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
                break

            data = response.json()
            results = data.get('results', [])
            all_donations.extend(results)

            print(f"   Fetched {len(results)} records... (Total: {len(all_donations)})")

            # 2. Check for Pagination
            pagination = data.get('pagination', {})
            last_indexes = pagination.get('last_indexes')

            if not last_indexes:
                break  # No more pages

            params.update(last_indexes)

            # Be nice to the API
            time.sleep(0.2)

        print(f"\nTotal {self.company} Donations found in {CYCLE}: {len(all_donations)}\n")
        return all_donations


    def getPaidMembers(self, bill_slug):

        def is_same_person(member_full_name, recipient_string):
            mem = HumanName(member_full_name)
            rec = HumanName(recipient_string)

            if mem.last.upper() != rec.last.upper():
                if mem.last.upper() not in recipient_string.upper():
                    return False

            if rec.first:

                if fuzz.ratio(mem.first.upper(), rec.first.upper()) < 80:
                    return False

            return True

        def splitSlug(slug):
            if slug.lower().startswith("hr"):
                return ["hr", slug[2:]]
            elif slug.lower().startswith("s"):
                return ["s", slug[1:]]
            return [slug[:2], slug[2:]]

        split = splitSlug(bill_slug)

        bill = Bill("118", split[0], split[1])
        if bill.id is None:
            return
        committee = Committee(bill.id, bill.chamber, "118")

        paidMembers = []

        for donation in self.donations:
            amount = donation.get('disbursement_amount', 0)
            if amount <= 0: continue

            recipient_identities = []

            if donation.get('candidate_name'):
                recipient_identities.append(donation['candidate_name'].upper())

            # Check for hidden Leadership PAC connections
            if donation.get('recipient_committee') and donation['recipient_committee'].get('affiliated_committee_name'):
                recipient_identities.append(donation['recipient_committee']['affiliated_committee_name'].upper())

            if donation.get('recipient_name'):
                recipient_identities.append(donation['recipient_name'].upper())

            # 2. Check Against Committee Members
            for member in committee.members:
                full_name = member['name']

                # Run the Smart Matcher
                match_found = False
                for identity in recipient_identities:
                    if is_same_person(full_name, identity):
                        match_found = True
                        break  # Found a match for this identity, stop checking identities

                if match_found:
                    paidMembers.append({
                        'member_name': full_name,
                        'member_id': member['bioguide'],
                        'amount': amount,
                        'date': donation.get('disbursement_date'),
                        'recipient_group': donation.get('recipient_name'),
                        'type': 'Direct' if donation.get('candidate_name') else 'PAC/Leadership'
                    })
                    break  # Stop checking members, this donation is claimed.

        return [paidMembers, bill]

    def beenPaid(self,name):
        pass
def get_company_logo(company_name):
    clean_name = company_name.lower()
    remove_words = [" llc", " inc", " corp", " corporation", " ltd", " company"]
    for word in remove_words:
        clean_name = clean_name.replace(word, "")

    clean_name = clean_name.strip().replace(" ", "")
    domain = f"{clean_name}.com"
    logo_url = f"https://unavatar.io/{domain}"

    return logo_url





#b = Bill("119","hr","1503")
#c = Committee(b.id, b.chamber,"119")

#l = Lobbying("AMAZON LLC")





TradeGroups = ['Technology Network (TechNet)']

for group in TradeGroups:
    Lobbying(group)
    print("-----------------")



