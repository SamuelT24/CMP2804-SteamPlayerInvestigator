from scoring import calculate_smurf_score, classify_account
from config import Classifications

#test calculate_smurf_score function
def test_calculate_smurf_score(): 
    user_info = {"account_age" : 300}
    friend_count = 20
    games_owned = 7
    playtime = 5000
    vac_ban = 0
    expected_score = 4

    assert calculate_smurf_score(user_info, friend_count, games_owned, playtime, vac_ban) == expected_score

#test classify_account function
def test_classify_account():
    assert classify_account(2) == Classifications.LIKELY_GENUINE
    assert classify_account(10) == Classifications.LIKELY_SMURF
    


