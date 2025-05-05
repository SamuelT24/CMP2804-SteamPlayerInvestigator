# CMP2804-SteamPlayerInvestigator

IMPORTANT!:
-> python.exe -m pip install requirements.txt
-> Run the project via Main.py
-> make sure not to upload your steam api key (purpose of .gitignore)

project overview: 

Steam Player Investigator is a project that will try to create a solution that determines whether a steam account is an alt account/secondary account

---

Config.yaml: A config file for your steam API key, and for all of the steam user IDs you wish to analyse. This is generated after running the program for the first time.

steam_api.py: Contains the "SteamAPI" class which manages communication with the Steam API to retrieve player info, friend lists, owned games, and ban data.

helpers.py: Contains utility functions to parse and format data from the API responses.

scoring.py: Implements the logic to calculate the smurf score.

config.py: Defines all the thresholds and penalty values used in scoring. Adjust these values to find how we want accounts to be judged.

main.py: The main script. It reads Steam IDs from Config.yaml, processes each account concurrently, and outputs a detailed report

frontend.py: Manages our user window.

---