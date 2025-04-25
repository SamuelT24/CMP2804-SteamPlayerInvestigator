from unittest.mock import patch, mock_open, MagicMock  
from Main import read_steam_ids, process_steam_id

#test read_steam_ids function
def test_read_steam_ids():
    mock_data = "111111111111111111\n222222222222222222"  
    with patch("builtins.open", mock_open(read_data=mock_data)): 
        result = read_steam_ids()
        
        assert result == ["111111111111111111", "222222222222222222"]

#test process_steam_id function
def test_process_steam_id():
    mock_api = MagicMock()  
    mock_api.get_player_info.return_value = {"response": {"players": [{"steamid": "id"}]}}
    mock_api.get_friend_list.return_value = {"friends_list": {"friends": [{}]}}
   
    with patch("Main.parse_user_info", return_value={"personaname": "TestUser", "account_age": 1}), \
         patch("Main.parse_friend_count", return_value=1), \
         patch("Main.calculate_smurf_score", return_value=2):

        user_info = process_steam_id("id", mock_api)

        assert user_info["personaname"] == "TestUser"
        assert user_info["account_age"] == 1
        assert user_info["friend_count"] == 1
        assert user_info["smurf_score"] == 2
