import os
import requests
from dotenv import load_dotenv

"""
steam_api.py handles the fetching and formatting of API calls 
"""
# Load environment variables from .env
load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    raise ValueError("STEAM_API_KEY not found in .env file.")

BASE_URL = "https://api.steampowered.com/"

class SteamAPI:
    def __init__(self):
        self.api_key = STEAM_API_KEY
        self.base_url = BASE_URL

    def get_player_info(self, steam_id):
    # Fetch player summary info from the steam API
        endpoint = "ISteamUser/GetPlayerSummaries/v2/"
        params = {
            "key": self.api_key,
            "steamids": steam_id
        }
        url = self.base_url + endpoint
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching player info for Steam ID {steam_id}.")
            return None

    def get_friend_list(self, steam_id):
    # Fetch friend list for the given steam ID
        endpoint = "ISteamUser/GetFriendList/v1/"
        params = {
            "key": self.api_key,
            "steamid": steam_id,
            "relationship": "friend"
        }
        url = self.base_url + endpoint
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching friend list for Steam ID {steam_id}.")
            return None
        
    def get_owned_games(self, steam_id):
    # Fetch owned games and playtime data from the Steam API
            endpoint = "IPlayerService/GetOwnedGames/v1/"
            params = {
                "key": self.api_key,
                "steamid": steam_id,
                "include_appinfo": "true",
                "include_played_free_games": "true"
            }
            url = self.base_url + endpoint
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching owned games for Steam ID {steam_id}.")
                return None

    def get_bans(self, steam_id):
    # Fetch ban information for the given Steam ID
        endpoint = "ISteamUser/GetPlayerBans/v1/"
        params = {
            "key": self.api_key,
            "steamids": steam_id
        }
        url = self.base_url + endpoint
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching bans for Steam ID {steam_id}.")
            return None