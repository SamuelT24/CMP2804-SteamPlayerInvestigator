from datetime import datetime

"""
helpers.py contains functions to process and format the raw data from API.
"""

def unix_to_date(timestamp):
# Convert a Unix timestamp to a simple date string
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except Exception:
        return "N/A"

def parse_user_info(raw_data):
# Extract basic user info from raw Steam API response
# Returns a dict with Steam ID, account creation date and account age in days
    players = raw_data.get("response", {}).get("players", [])
    if not players:
        return None
    player = players[0]
    creation_timestamp = int(player.get("timecreated", 0))
    creation_date = unix_to_date(creation_timestamp)
    account_age = "N/A"
    if creation_timestamp:
        account_age = (datetime.now() - datetime.fromtimestamp(creation_timestamp)).days
    return {
        "steam_id": player.get("steamid", "Unknown"),
        "personaname": player.get("personaname", "Unknown"),
        "creation_date": creation_date,
        "account_age": account_age
    }

def format_report(user_info):
# Returns a formatted report string for the given user info
    if not user_info:
        return "No user data available."
    report = (
        f"Name: {user_info.get("personaname")}\n"
        f"Steam ID: {user_info.get("steam_id")}\n"
        f"Account Created: {user_info.get("creation_date")}\n"
        f"Account Age (days): {user_info.get("account_age")}\n"
    )
    return report

def parse_friend_count(raw_data):
# Extract the number of friends from the raw friend list API response

    friends = raw_data.get("friendslist", {}).get("friends", [])
    return len(friends) if friends else 0

def parse_vac_ban(raw_data):
# Determine whether the account is VAC banned. Returns 1 if banned and if not then 0
    players = raw_data.get("players", [])
    if players and players[0].get("VACBanned", False):
        return 1
    return 0

def parse_owned_games(raw_data):
# Extract number of games owned and total playtime from the raw owned games API response
    games = raw_data.get("response", {}).get("games", [])
    number_of_games = len(games)
    total_playtime = sum(game.get("playtime_forever", 0) for game in games)
    return number_of_games, total_playtime

