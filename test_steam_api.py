
"""
Unit tests for steam_api.py
Uses monkey patch to stub out HTTP requests
"""
import os
import pytest
from steam_api import SteamAPI

# Ensure we have a dummy API key so importing SteamAPI wont raise
os.environ.setdefault("STEAM_API_KEY", "DUMMY")

class FakeResp:
    def __init__(self, code, data):
        self.status_code = code
        self._data = data
    def json(self):
        return self._data
    def raise_for_status(self):
        pass

def fake_get(url, params=None, timeout=None):
    if "GetPlayerSummaries" in url: # Simulate a successful player summary
        return FakeResp(200, {"response": {"players": [{"steamid": params["steamids"]}]}})
    if "GetFriendList" in url: # Simulate a friend list with one entry
        return FakeResp(200, {"friendslist": {"friends": [{}]}})
    if "GetOwnedGames" in url: # Simulate owned games list with a 3 minute playtime
        return FakeResp(200, {"response": {"games": [{"playtime_forever": 3}]}})
    if "GetPlayerBans" in url: # Simulate ban data with VACBanned = False
        return FakeResp(200, {"players": [{"VACBanned": False}]})
    return FakeResp(404, {}) # Default to “not found"

# Automatically replace requests.get in steam_api with fake_get before each test runs
@pytest.fixture(autouse=True) 
def patch_requests(monkeypatch):
    import steam_api
    monkeypatch.setattr(steam_api.requests, "get", fake_get)


# Verify that get_player_info returns the fake steamid from stub
def test_get_player_info_success():
    api = SteamAPI()
    data = api.get_player_info("XYZ")
    assert data["response"]["players"][0]["steamid"] == "XYZ"


# Verify that get_friend_list returns a list of friends
def test_get_friend_list_success():
    api = SteamAPI()
    data = api.get_friend_list("XYZ")
    assert isinstance(data["friendslist"]["friends"], list)


# Verify that get_owned_games returns the fake playtime
def test_get_owned_games_success():
    api = SteamAPI()
    data = api.get_owned_games("XYZ")
    assert data["response"]["games"][0]["playtime_forever"] == 3


# Verify that get_bans returns the fake VACBanned status
def test_get_bans_success(): 
    api = SteamAPI()
    data = api.get_bans("XYZ")
    assert data["players"][0]["VACBanned"] is False


# Simulate a HTTP 500 errors for all endpoints, ensure the SteamAPI methods return {} on failure
def test_error_responses(monkeypatch):
    import steam_api
    def always_fail(url, params):
        return FakeResp(500, {})
    
    def always_fail(url, params=None, timeout=None):
        return FakeResp(500, {})

    monkeypatch.setattr(steam_api.requests, "get", always_fail)

    api = SteamAPI()
    assert api.get_player_info("1") == {}
    assert api.get_friend_list("1") == {}
    assert api.get_owned_games("1") == {}
    assert api.get_bans("1") == {}
