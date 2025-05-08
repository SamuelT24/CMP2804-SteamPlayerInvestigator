import logging
import requests
import user_config

"""
steam_api.py handles the fetching and formatting of API calls 
"""

STEAM_API_KEY = user_config.api_key

BASE_URL = "https://api.steampowered.com/"

class SteamAPI:
    def __init__(self) -> None:
        self.log = logging.getLogger(__class__.__name__)
        self.api_key = STEAM_API_KEY
        self.base_url = BASE_URL

    def _fetch(self, endpoint: str, params: dict) -> dict:
        # Helper to get_ functions from Steam API with error handling, returns parsed JSON on success or {} on failures
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()    # raises for HTTP 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            self.log.error(f"[SteamAPI] {endpoint} failed: {e}")
            return {}
        
    def get_player_info(self, steam_id:str) -> dict:
        # Fetch player summary info from the steam API
        return self._fetch(
            "ISteamUser/GetPlayerSummaries/v2/",
            {"key": self.api_key, "steamids": steam_id}
        )

    def get_friend_list(self, steam_id:str) -> dict:
        # Fetch friend list for the given steam ID
        return self._fetch(
            "ISteamUser/GetFriendList/v1/",
            {"key": self.api_key, "steamid": steam_id, "relationship": "friend"}
        )
        
    def get_owned_games(self, steam_id:str) -> dict:
        # Fetch owned games and playtime data from the Steam API
            return self._fetch(
            "IPlayerService/GetOwnedGames/v1/",
            {
                "key": self.api_key,
                "steamid": steam_id,
                "include_appinfo": "true",
                "include_played_free_games": "true"
            }
        )

    def get_bans(self, steam_id:str) -> dict:
        return self._fetch(
            "ISteamUser/GetPlayerBans/v1/",
            {"key": self.api_key, "steamids": steam_id}
        )