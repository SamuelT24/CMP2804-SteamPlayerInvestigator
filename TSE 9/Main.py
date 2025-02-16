import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

class SteamAPI: #loads enviroment variables from env file
    def __init__(self):
        """Initialize Steam API client"""
        load_dotenv()
        self.api_key = os.getenv('STEAM_API_KEY')
        if not self.api_key:
            raise ValueError("STEAM_API_KEY not found in environment variables")
        self.base_url = "https://api.steampowered.com/"

    def _get_data(self, endpoint, params): 
        """Make API request with error handling"""
        try:
            params['key'] = self.api_key
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error accessing Steam API: {e}")
            return None

    def get_player_info(self, steam_id):
        """Get player profile data"""
        return self._get_data("ISteamUser/GetPlayerSummaries/v2", {"steamids": steam_id})

    def get_friend_list(self, steam_id):
        """Get friend list data"""
        return self._get_data("ISteamUser/GetFriendList/v1", 
                             {"steamid": steam_id, "relationship": "friend"})

    def get_owned_games(self, steam_id):
        """Get owned games data"""
        return self._get_data("IPlayerService/GetOwnedGames/v1", 
                             {"steamid": steam_id, "include_appinfo": "true", "include_played_free_games": "true"})

    def get_bans(self, steam_id):
        """Get ban information"""
        return self._get_data("ISteamUser/GetPlayerBans/v1", {"steamids": steam_id})


def unix_to_datetime(timestamp):
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        dt = dt.astimezone()
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return "Date unavailable"


def format_playtime(minutes):
    """Convert playtime from minutes to hours and minutes"""
    if minutes == 0:
        return "Never played"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if hours == 0:
        return f"{remaining_minutes}m"
    elif remaining_minutes == 0:
        return f"{hours}h"
    else:
        return f"{hours}h {remaining_minutes}m"


def display_profile(data):
    """Display Steam profile information"""
    if not data or 'response' not in data or not data['response']['players']:
        print("Profile not found or private")
        return

    player = data['response']['players'][0]
    print("\n=== Steam Profile ===")
    print(f"Name: {player.get('personaname', 'N/A')}")
    if 'timecreated' in player:
        print(f"Account Created: {unix_to_datetime(player['timecreated'])}")
    print(f"Profile URL: {player.get('profileurl', 'N/A')}")

    if player.get('communityvisibilitystate', 0) != 3:
        print("Note: This profile is private")


def display_friends(data):
    """Display friend count"""
    if not data or 'friendslist' not in data:
        print("\nFriends list private or unavailable")
        return

    friends = data['friendslist']['friends']
    print(f"\nFriend Count: {len(friends)}")


def display_games(data):
    """Display detailed games information"""
    if not data or 'response' not in data:
        print("\nGames list private or unavailable")
        return

    games = data['response'].get('games', [])
    total_games = len(games)
    
    print(f"\n=== Games Owned: {total_games} ===")
    
    if total_games == 0:
        return

    # Sort games by playtime
    games.sort(key=lambda x: x.get('playtime_forever', 0), reverse=True)

    # Calculate total playtime
    total_playtime = sum(game.get('playtime_forever', 0) for game in games)
    print(f"Total Playtime: {format_playtime(total_playtime)}")
    
    print("\nGame List (sorted by playtime):")
    print("-" * 60)
    print(f"{'Name':<40} {'Playtime':<15} {'Last Played':<20}")
    print("-" * 60)

    for game in games:
        name = game.get('name', 'Unknown Game')
        playtime = format_playtime(game.get('playtime_forever', 0))
        
        # Convert last played timestamp
        last_played = game.get('rtime_last_played', 0)
        if last_played > 0:
            last_played_str = unix_to_datetime(last_played)
        else:
            last_played_str = "Never"

        # Truncate long game names
        if len(name) > 37:
            name = name[:34] + "..."

        print(f"{name:<40} {playtime:<15} {last_played_str:<20}")


def display_bans(data):
    """Display ban information"""
    if not data or not data.get('players'):
        print("\nBan data unavailable")
        return

    player = data['players'][0]
    print("\n=== Ban Status ===")
    print(f"VAC Banned: {player.get('VACBanned', 'No')}")
    print(f"VAC Bans: {player.get('NumberOfVACBans', 0)}")


def main():
    """Main function"""
    try:
        api = SteamAPI()
    except ValueError as e:
        print(f"Error: {e}")
        return

    while True:
        steam_id = input("\nEnter Steam ID (or 'exit' to quit): ").strip()
        if steam_id.lower() == 'exit':
            break
        if not steam_id:
            continue

        print("\nFetching data...")
        
        # Get and display profile data
        profile = api.get_player_info(steam_id)
        display_profile(profile)

        # Get and display additional data
        friends = api.get_friend_list(steam_id)
        display_friends(friends)

        games = api.get_owned_games(steam_id)
        display_games(games)

        bans = api.get_bans(steam_id)
        display_bans(bans)

        print("\n=== End of Report ===")
        


if __name__ == "__main__":
    main()