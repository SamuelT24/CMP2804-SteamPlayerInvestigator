"""
Configuration file for scoring.py

This file contains thresholds and penalty values for evaluating Steam accounts.
Each section is organised by the what it affects.
"""

# Scoring thresholds and penalties for absolute metrics
SCORE = {
    # Account age, in days
    "account_age": {
        "penalty_zero_age": 5,               # Penalty if the account age is zero
        "threshold_high_penalty": 180,       # If account age is less than 180 days, receives a high penalty
        "penalty_high": 3,                   # Penalty for accounts younger than 180 days
        "threshold_medium_penalty": 365,     # Account age less than 365 days receives a medium penalty
        "penalty_medium": 2,                 # Penalty for accounts between 180 and 365 days old
        "penalty_low": 0                     # No penalty for accounts older than 365 days
    },
    
    # Friend count
    "friend_count": {
        "threshold_low": 10,        # Fewer than 10 friends
        "penalty_low": 2,           # Penalty if friend count is low
        "threshold_medium": 30,     # Between 10 and 30 friends
        "penalty_medium": 1         # Penalty if friend count is at medium threshold
    },

    # Games owned
    "games_owned": {
        "threshold_low": 5,         # Fewer than 5 games owned
        "penalty_low": 2,           # Penalty if few games are owned
        "threshold_medium": 10,     # Between 5 and 10 games owned
        "penalty_medium": 1         # Penalty if game count is at medium threshold
    },

    # Total playtime, in minutes
    "playtime": {
        "threshold_low": 500,          # Under 500 minutes of total playtime
        "penalty_low": 3,              # Penalty if playtime is very low
        "threshold_medium": 2000,      # Between 500 and 2000 minutes
        "penalty_medium": 2            # Penalty if playtime is at medium threshold
    },

    # VAC ban penalty
    "vac": {
        "penalty": 5  # Heavy penalty if the account is VAC banned
    }
}

# General settings for classification
GENERAL = {
    "smurf_score_threshold": 6   # Final threshold for classifying an account as smurf
}
