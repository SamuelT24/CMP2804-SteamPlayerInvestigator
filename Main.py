from steam_api import SteamAPI
from helpers import (parse_user_info, format_report, parse_friend_count,parse_owned_games, parse_vac_ban)
from scoring import calculate_smurf_score, classify_account
from concurrent.futures import ThreadPoolExecutor

def read_steam_ids(file_path="steam_ids.txt"):
# Read Steam IDs from the file one per line
    try:
        with open(file_path, "r") as f:
            ids = [line.strip() for line in f if line.strip()]
        return ids
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def process_steam_id(steam_id, api):
    print(f"\nFetching data for Steam ID: {steam_id}")
        
    # Fetch player info and parse basic data
    raw_data = api.get_player_info(steam_id) 
    user_info = parse_user_info(raw_data)

    # Fetch friends list number
    friend_data = api.get_friend_list(steam_id)
    friend_count = parse_friend_count(friend_data)
        
    # Fetch owned games info and total playtime
    games_data = api.get_owned_games(steam_id)
    number_of_games, total_playtime = parse_owned_games(games_data)

    # Fetch ban information and determine VAC ban status
    bans_data = api.get_bans(steam_id)
    vac_ban = parse_vac_ban(bans_data)

    # Fetches the clasification results
    score = calculate_smurf_score(user_info, friend_count, number_of_games, total_playtime, vac_ban)
    classification = classify_account(score)

    # Prints the combined report
    print("User Info:")
    print(format_report(user_info))
    print(f"Friend Count: {friend_count}")
    print(f"Number of Games Owned: {number_of_games}")
    print(f"Total Playtime (minutes): {total_playtime}")
    print(f"VAC Banned: {vac_ban}")
    print(f"Smurf Score: {score}")
    print(f"Classification: {classification}")
    print("-" * 40)
    
def main():
    steam_ids = read_steam_ids()
    if not steam_ids:
        print("No Steam IDs to process.")
        return

    api = SteamAPI()

    # Using ThreadPoolExecutor to process Steam IDs concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        for steam_id in steam_ids:
            executor.submit(process_steam_id, steam_id, api)

if __name__ == "__main__":
    main()
