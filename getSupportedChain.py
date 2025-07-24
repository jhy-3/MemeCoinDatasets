import requests
import json

API_URL = "https://prod.ave-api.com/v2/supported_chains"
API_KEY = "HPmf6KfmMkNWWwcItyvPKHtv4BVCpM7gZU1JYsE7xwQcJqx41G6V5xKUdYCuMvvR"
OUTPUT_PATH = "tokenDatasets/getSupportChain.json"


def fetch_and_save_supported_chains():
    headers = {
        "X-API-KEY": API_KEY
    }
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved supported chains to {OUTPUT_PATH}")


if __name__ == "__main__":
    fetch_and_save_supported_chains()
