import logging
import os
import sys
import time
import traceback

from concurrent.futures import ThreadPoolExecutor
from frontend import SmurfDetectorApp
from helpers import (parse_user_info, format_report, parse_friend_count,parse_owned_games, parse_vac_ban)
from scoring import calculate_smurf_score, classify_account
from steam_api import SteamAPI

# Create logs directory then configure our logging system
os.makedirs("logs", exist_ok=True)

localtime = time.localtime()
log_suffix = "%02d%02d%02d_%02d%02d%02d" % (localtime[0] - 2000,  localtime[1], localtime[2],
                                           localtime[3], localtime[4], localtime[5])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(f"logs/SPInvestigatorD-{log_suffix}.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# All logging output using this logger will be under this name
log = logging.getLogger("SteamPlayerInvestigatorBase")

def read_steam_ids(file_path:str="steam_ids.txt") -> list[str]:
    # Read Steam IDs from the file one per line
    try:
        with open(file_path, "r") as f:
            ids = [line.strip() for line in f if line.strip()]
        return ids
    except FileNotFoundError:
        log.error(f"Error: File \"{file_path}\" not found.")
        return []

def process_steam_id(steam_id:str, api:SteamAPI) -> dict:
    log.info(f"\nFetching data for Steam ID: {steam_id}")
        
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

    # Outputs the combined report
    additional_info = f"Friend Count: {friend_count}\nNumber of Games Owned: {number_of_games}\nTotal Playtime (minutes): {total_playtime}\nVAC Banned: {vac_ban}\nSmurf Score: {score}\nClassification: {classification}"
    log.info(f'User Info:\n{"-" * 40}\n{format_report(user_info)}\n{additional_info}\n{("-" * 40)}')
    
    return (user_info or {}) | {
        "friend_count": friend_count,
        "games_owned": number_of_games,
        "playtime": total_playtime,
        "vac_banned": vac_ban,
        "smurf_score": score,
        "classification": classification
                        }

def get_all_user_info_futures() -> list[dict]:
    """concurrently adds user details to a list as futures which is then 
    returned in order to give the UI information about the users"""

    steam_ids = read_steam_ids()
    if not steam_ids:
        log.warning("No Steam IDs to process.")
        return []

    api = SteamAPI()
    future_list = []
    # Using ThreadPoolExecutor to process Steam IDs concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        for steam_id in steam_ids:
            """futures represent a result of information that hasn't happened yet, used
            to schedule multiple tasks and in a clean way"""
            future = executor.submit(process_steam_id, steam_id, api)
            future_list.append(future)

    return [future.result() for future in future_list]

def handle_exception(exc_type, exc_value, exc_traceback):
    # Mostly future proofing if we ever wanted to do something special instead of crashing out,
    # but also so the exception is outputting to our log file.
    if issubclass(exc_type, KeyboardInterrupt):
        log.info("Program has been exited via terminal.")
        return
    
    log.error(f"Encountered exception: {exc_value}\n\n{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}")
    sys.exit(1)

if __name__ == "__main__":
    sys.excepthook = handle_exception
    app = SmurfDetectorApp(get_all_user_info_futures())
    app.mainloop()
