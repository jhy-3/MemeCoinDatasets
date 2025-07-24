import requests
import json
import os

API_KEY = "79570410-a0e3-4ca1-81f9-9c0626f0e31a"
URL = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/latest"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "fearAndGreed.json")

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,
}

def fetch_fear_and_greed():
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    return response.json()

def save_to_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    data = fetch_fear_and_greed()
    save_to_json(data, OUTPUT_PATH)
    print(f"Saved latest Fear and Greed Index to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
