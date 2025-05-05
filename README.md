# CMP2804-SteamPlayerInvestigator

Steam Player Investigator is a project that will try to create a solution that determines whether a steam account is an alternate/"smurf" account.


## How to run

-> python -m pip install -r requirements.txt

-> python -m Main

Once a Config.yaml file has been generated, open it and set your api_key to your Steam API key. This application will not work without it. You can also change the IDs the program investigates, and whether you want dark mode enabled or disabled for the GUI.

## Project overview

Config.yaml: A config file for your steam API key, and for all of the steam user IDs you wish to analyse. This is generated after running the program for the first time.

user_config.py: This file reads the Config.yaml file and generates a default user config where necessary.

steam_api.py: Contains the "SteamAPI" class which manages communication with the Steam API to retrieve player info, friend lists, owned games, and ban data.

helpers.py: Contains utility functions to parse and format data from the API responses.

scoring.py: Implements the logic to calculate the smurf score.

config.py: Defines all the thresholds and penalty values used in scoring. Adjust these values to find how we want accounts to be judged.

main.py: The main script. It reads Steam IDs from Config.yaml, processes each account concurrently, and outputs a detailed report

frontend.py: Manages our user window.

Any file with a "test_" prefix is for testing purposes, and not part of the main application.

## Credits

John Atanbori - Project Supervisor

Samuel Tracey (26392615)

Anthony Johns (27948530)

Oliver Niles (27704554)

Riaz Ali (28689348)

Scott Johnson (26579696)

Zak Knell (26577836)


Steam (https://steamcommunity.com/) for their API, used to collect account data.