import requests
import json
import time

API_KEY = "SkSKVNdUY7SbvpE1ozuwxuZWn2RQlUMU0IAcGAOHCfTvDKkd4dYBc0nx4XKUwRvm"
API_URL = "https://prod.ave-api.com/v2/tokens/{}"
HEADERS = {"X-API-KEY": API_KEY}
INPUT_FILE = "tokenDatasets/searchToken.json"
OUTPUT_FILE = "tokenDatasets/getTokenDetail.json"

def read_token_ids(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        token_lines = lines[1:]  # skip header
        tokens = []
        for line in token_lines:
            try:
                data = json.loads(line)
                token_id = f"{data['token']}-{data['chain']}"
                tokens.append(token_id)
            except Exception:
                continue
    return tokens

def fetch_token_detail(token_id, retries=3, delay=1):
    url = API_URL.format(token_id)
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"token_id": token_id, "error": resp.status_code, "body": resp.text}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return {"token_id": token_id, "error": str(e)}

def save_results(results, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def main():
    tokens = read_token_ids(INPUT_FILE)
    results = []
    try:
        for idx, token_id in enumerate(tokens):
            result = fetch_token_detail(token_id)
            results.append(result)
            print(f"[{idx+1}/{len(tokens)}] {token_id} done.")
            time.sleep(0.5)  # avoid rate limits
    except KeyboardInterrupt:
        print("手动中断，正在保存已获取的数据...")
    save_results(results, OUTPUT_FILE)
    print("已保存到", OUTPUT_FILE)

if __name__ == "__main__":
    main()
