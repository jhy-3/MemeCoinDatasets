import requests
import json
import os

API_URL = "https://prod.ave-api.com/v2/ranks/topics"
API_KEY = "SkSKVNdUY7SbvpE1ozuwxuZWn2RQlUMU0IAcGAOHCfTvDKkd4dYBc0nx4XKUwRvm"
OUTPUT_PATH = os.path.join("tokenDatasets", "getTokenRankTopics.json")

headers = {
    "X-API-KEY": API_KEY
}

def main():
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved response to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
