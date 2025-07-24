import json
import requests
import os

API_KEY = "HPmf6KfmMkNWWwcItyvPKHtv4BVCpM7gZU1JYsE7xwQcJqx41G6V5xKUdYCuMvvR"
API_URL_TEMPLATE = "https://prod.ave-api.com/v2/klines/pair/{pair_id}?interval={interval}&limit={limit}"

SEARCH_TOKEN_PATH = os.path.join("tokenDatasets", "searchToken.json")
OUTPUT_PATH = os.path.join("tokenDatasets", "getKineDataByPair.json")

# Read the first 10 tokens from searchToken.json
with open(SEARCH_TOKEN_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()
    # The first line is the header, skip it
    tokens = []
    for line in lines[1:]:
        if line.strip():
            try:
                data = json.loads(line)
                tokens.append(data)
            except Exception:
                continue
        if len(tokens) >= 10:
            break

def get_kline_data(token, chain="solana", interval=1, limit=5):
    pair_id = f"{token['main_pair']}-{chain}"
    url = API_URL_TEMPLATE.format(pair_id=pair_id, interval=interval, limit=limit)
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': API_KEY
    }
    session = requests.Session()
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        # Attach the target_token_id for reference
        result['target_token_id'] = f"{token['token']}-{chain}"
        return result
    else:
        return {
            "status": 0,
            "msg": f"Failed to fetch for {token['token']}",
            "http_status": response.status_code,
            "target_token_id": f"{token['token']}-{chain}"
        }

results = []
for token in tokens:
    result = get_kline_data(token)
    results.append(result)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
