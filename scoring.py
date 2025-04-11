from config import SCORE, GENERAL

"""
Calculates a smurf score based on the account data
"""

def calculate_smurf_score(user_info, friend_count, number_of_games, total_playtime, vac_ban):

    score = 0
    
    # Score based on account age and is given in days
    account_age = user_info.get("account_age", 0)
    age_config = SCORE["account_age"]
    if account_age == 0:
        score += age_config["penalty_zero_age"]
    elif account_age < age_config["threshold_high_penalty"]:
        score += age_config["penalty_high"]
    elif account_age < age_config["threshold_medium_penalty"]:
        score += age_config["penalty_medium"]
    else:
        score += age_config["penalty_low"]

    # Score based on the friend count
    friend_config = SCORE["friend_count"]
    if friend_count < friend_config["threshold_low"]:
        score += friend_config["penalty_low"]
    elif friend_count < friend_config["threshold_medium"]:
        score += friend_config["penalty_medium"]


    # Score based on the number of games owned
    games_config = SCORE["games_owned"]
    if number_of_games < games_config["threshold_low"]:
        score += games_config["penalty_low"]
    elif number_of_games < games_config["threshold_medium"]:
        score += games_config["penalty_medium"]

    # Score based on total playtime which is in minutes
    playtime_config = SCORE["playtime"]
    if total_playtime < playtime_config["threshold_low"]:
        score += playtime_config["penalty_low"]
    elif total_playtime < playtime_config["threshold_medium"]:
        score += playtime_config["penalty_medium"]

    # Add a heavy penalty if account is VAC banned
    if vac_ban == 1:
        score += SCORE["vac"]["penalty"]

    return score

def classify_account(score, threshold=None):
    if threshold is None:
        threshold = GENERAL["smurf_score_threshold"]
    return "Likely Smurf Account" if score >= threshold else "Likely Genuine Account"
