import json
import os

def get_user_rules() -> dict:
    if os.path.exists("user_data/rules.json"):
        with open("user_data/rules.json", "r") as f:
            return json.load(f)

def get_user_rates() -> dict:
    if os.path.exists("user_data/rates.json"):
        with open("user_data/rules.json", "r") as f:
            return json.load(f)