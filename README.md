# CMP2804-SteamPlayerInvestigator

IMPORTANT!: 
-> run from frontend.py in this version
-> make sure not to upload your steam api key (purpose of .gitignore)

project overview: 

Steam Player Investigator is a project that will try to create a solution that determines whether a steam account is an alt account/secondary account

---

env: Stores environment variables, including your Steam API key.

steam_ids.txt: A text file Storing the Steam IDs you wish to analyze (one per line).

steam_api.py: Contains the "SteamAPI" class which manages communication with the Steam API to retrieve player info, friend lists, owned games, and ban data.

helpers.py: Contains utility functions to parse and format data from the API responses.

scoring.py: Implements the logic to calculate the smurf score.

config.py: Defines all the thresholds and penalty values used in scoring. Adjust these values to find how we want accounts to be judged.

main.py: The main script. It reads Steam IDs from steam_ids.txt, processes each account concurrently, and outputs a detailed report

---