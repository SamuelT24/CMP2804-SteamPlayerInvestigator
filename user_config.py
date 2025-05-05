import logging
import os
import sys
import yaml

log = logging.getLogger("UserConfig")


def create_default_config() -> None:
    default_config = {"api_key": "SETME", # The user has to set their own steam API key.
                      "steam_user_ids_to_investigate": [76561198880957262, 76561199830603993, 76561199549086373, # Just some default users to test
                                                        76561198859184395, 76561198051496316, 76561198049635812,
                                                        76561197972029133, 76561198102830296, 76561198237596866,
                                                        76561198153094237, 76561198326195257, 76561198119528593,
                                                        76561198092022583, 76561198088795597, 76561198962788952,
                                                        76561198853947008, 76561198845422822, 76561198131858486,
                                                        76561198158749938, 76561198217138088, 76561198271352236,
                                                        76561198193335986, 76561198132623523, 76561198170376067,
                                                        76561198058696022, 76561198209358256, 76561198244515154,
                                                        76561198259055702, 76561198334113296],
                      "dark_mode": True,}
    with open("Config.yaml", "w") as f:
        yaml.safe_dump(default_config, f, sort_keys=False, default_flow_style=False)

if os.path.exists("Config.yaml"):
    with open("Config.yaml", "r") as f:
        config = yaml.safe_load(f)
    try:
        globals().update(config)
    except:
        log.error("Config.yaml has invalid data. A new one will be generated for you. Please reconfigure and try again.")
        os.remove("Config.yaml")
        create_default_config()
        sys.exit(1)

else:
    log.error("Config.yaml is missing. A new one will be generated for you. Please reconfigure and try again.")
    create_default_config()
    sys.exit(1)