import json
import requests
import os

API_KEY = "HPmf6KfmMkNWWwcItyvPKHtv4BVCpM7gZU1JYsE7xwQcJqx41G6V5xKUdYCuMvvR"
API_URL = "https://prod.ave-api.com/v2/tokens/top100/{}"
HEADERS = {"X-API-KEY": API_KEY}
SEARCH_TOKEN_PATH = os.path.join("tokenDatasets", "searchToken.json")
OUTPUT_PATH = os.path.join("tokenDatasets", "getTokenTop100Holders.json")

# Step 1: Read the first 10 token+chain pairs from searchToken.json
def get_first_10_token_ids():
    token_ids = []
    with open(SEARCH_TOKEN_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # skip the first line (header)
        for line in lines[1:11]:
            try:
                obj = json.loads(line)
                token = obj["token"]
                chain = obj["chain"]
                token_ids.append(f"{token}-{chain}")
            except Exception as e:
                continue
    return token_ids

# Step 2: Fetch top 100 holders for each token_id
def fetch_top100(token_id):
    url = API_URL.format(token_id)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"token_id": token_id, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"token_id": token_id, "error": str(e)}


def main():
    token_ids = get_first_10_token_ids()
    results = []
    for token_id in token_ids:
        print(f"Fetching {token_id} ...")
        data = fetch_top100(token_id)
        # Optionally, add token_id to each result for clarity
        if isinstance(data, dict) and "data" in data:
            data["token_id"] = token_id
        results.append(data)
    # Save as JSON
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved results to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
