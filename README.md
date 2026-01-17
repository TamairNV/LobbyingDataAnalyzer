# LobbyingDataAnalyzer
A Python tool that connects corporate lobbying data to legislative targets. It automates the process of linking lobbying disclosures to specific bills, identifying the committee in charge, and pinpointing the members of Congress who control those committees.

How It Works
The script follows a four-step pipeline to reveal where corporate influence is directed:

Lobbying Report: Extracts bill numbers (e.g., H.R. 1843) from Senate LDA filings.

Bill Data: Uses the Congress.gov API to identify the bill's subject and status.

Committee Assignment: Locates the specific House or Senate committee that controls the bill.

Member Targeting: Generates a list of committee members (Chairs and Ranking Members) who are the primary targets for PAC donations.
