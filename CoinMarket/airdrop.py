import requests
import json
import os

# Set your API key here
API_KEY = "79570410-a0e3-4ca1-81f9-9c0626f0e31a"

# API endpoint
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/airdrop"

# Output file path
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "coinMarketData", "airdrop.json")

# Fixed airdrop id
AIRDROP_ID = "60e59b99c8ca1d58514a2322"

def fetch_airdrop(airdrop_id):
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY
    }
    params = {
        "id": airdrop_id
    }
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    data = fetch_airdrop(AIRDROP_ID)
    save_json(data, OUTPUT_PATH)
    print(f"Airdrop data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
