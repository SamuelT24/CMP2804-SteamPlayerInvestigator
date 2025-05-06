"""
Configuration file for scoring.py

This file contains thresholds and penalty values for evaluating Steam accounts.
Each section is organised by the what it affects.
"""

# Scoring thresholds and penalties for absolute metrics
SCORE = {
    # Account age, in days
    "account_age": {
        "penalty_zero_age": 5,      # Penalty if the account age is zero
        "threshold_very_low": 21,   # Account age less than 21 days
        "penalty_very_low": 4,      # Penalty if very low account age threshold is met
        "threshold_low": 180,       # Account age less than 180 days
        "penalty_low": 3,           # Penalty if low account age threshold is met
        "threshold_medium": 365,    # Account age less than 365 days
        "penalty_medium": 2,        # Penalty if medium account age threshold is met
        "threshold_high": 730,      # Account age less than 730 days 
        "penalty_high": 0           # No penalty if high account age threshold is met
    },
    
    # Friend count
    "friend_count": {
        "threshold_very_low": 5,    # Less than 5 friends
        "penalty_very_low": 5,      # Penalty if very low threshold is met
        "threshold_low": 30,        # Betwwen 5 and 30 friends
        "penalty_low": 2,           # Penalty if low threshold is met
        "threshold_medium": 70,     # Between 30 and 70 friends
        "penalty_medium": 1,        # Penalty if medium threshold is met
        "threshold_high": 150,      # Between 70 and 150 friends
        "penalty_high": 0           # No penalty if high threshold is met
    },

    # Games owned
    "games_owned": {
        "threshold_very_low": 2,    # Fewer than 2 games owned
        "penalty_very_low": 5,      # Penalty if very low games threshold is met
        "threshold_low": 20,        # Between 2 and 20 games owned
        "penalty_low": 2,           # Penalty if low games threshold is met
        "threshold_medium": 50,     # Between 20 and 50 games owned
        "penalty_medium": 1,        # Penalty if medium games threshold is met
        "threshold_high": 100,      # Between 50 and 100 games owned
        "penalty_high": 0           # No penalty if high games threshold is met
    },

    # Total playtime, in minutes
    "playtime": {
        "threshold_low": 6000,         # Under 6000 minutes (100 hours) of total playtime
        "penalty_low": 3,              # Penalty if low playtime threshold is met
        "threshold_medium": 30000,     # Between 6000 and 30000 minutes (100 and 500 hours) of total playtime
        "penalty_medium": 2,           # Penalty if medium playtime threshold is met
        "threshold_high": 120000,      # Between 30000 and 60000 minutes (500 and 2000 hours) of total playtime
        "penalty_high": 0,             # No penalty if high playtime threshold is met
        "penalty_very_high": -1        # If playtime is over 120000 minutes (2000 hours) then reduce smurf score
    },

    # VAC ban penalty
    "vac": {
        "penalty": 2  # penalty if the account is VAC banned
    }
}

# General settings for classification
GENERAL = {
    "smurf_score_threshold": 6   # Final threshold for classifying an account as smurf
}

from enum import Enum

class Classifications(Enum):
    LIKELY_SMURF = "Likely Smurf"
    LIKELY_GENUINE = "Likely Genuine"

    def __str__(self):
        return self.value