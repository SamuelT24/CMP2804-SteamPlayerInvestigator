

"""
test_helpers.py - Unit tests for helpers.py

"""

import os
from datetime import datetime
import pytest
from helpers import (
    parse_user_info,
    format_report,
    parse_friend_count,
    parse_vac_ban,
    parse_owned_games,
)

def test_parse_user_info_basic():
    # Given a known timestamp for 2021-01-01
    ts = 1609459200
    raw = {"response": {"players": [{"steamid": "123", "personaname": "Optimus Prime", "timecreated": ts}]}}
    info = parse_user_info(raw)
    assert info["steam_id"] == "123"
    assert info["personaname"] == "Optimus Prime"
    assert info["creation_date"] == "2021-01-01"
    assert isinstance(info["account_age"], int) # Ensures account_age is returned as an integer


# When no player data is present parse_user_info should then return the dummy defaults
def test_parse_user_info_empty():
    assert parse_user_info({"response": {"players": []}})["steam_id"] == "Unknown"
    assert parse_user_info(None)["account_age"] == 0


# Check that format_report generates the expected string and handles an empty dict
def test_format_report():
    user = {
        "steam_id": "321",
        "personaname": "Lebron",
        "creation_date": "2020-06-15",
        "account_age": 100
    }
    rpt = format_report(user)
    assert "Name: Lebron" in rpt
    assert "Account Age (days): 100" in rpt
    assert format_report({}) == "No user data available."


# Verify parse_friend_count returns the correct count of friends and returns 0 when passed an empty dict
def test_parse_friend_count():
    assert parse_friend_count({"friendslist": {"friends": [{}, {}]}}) == 2
    assert parse_friend_count({}) == 0


# Verify parse_vac_ban correctly identifies a VAC ban and parse_owned_games returns number_of_games, total_playtime
def test_parse_vac_ban_and_games():
    assert parse_vac_ban({"players": [{"VACBanned": True}]}) is True # VAC ban present
    num, total = parse_owned_games({"response": {"games": [{"playtime_forever": 10}, {"playtime_forever": 5}]}}) # Two games with 10 and 5 minutes playtime
    assert num == 2
    assert total == 15
    assert parse_owned_games({}) == (0, 0) 
