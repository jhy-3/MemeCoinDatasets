import requests
import json
import os

def get_first_10_token_ids(json_path):
    """
    从searchToken.json中获取前10个token_id（格式为{token}-{chain}）
    """
    token_ids = []
    with open(json_path, 'r', encoding='utf-8') as f:
        # 跳过第一行字段名
        next(f)
        for i, line in enumerate(f):
            if i >= 10:
                break
            data = json.loads(line)
            token = data.get('token')
            chain = data.get('chain')
            if token and chain:
                token_ids.append(f"{token}-{chain}")
    return token_ids

def fetch_risk_report(token_id, api_key):
    url = f"https://prod.ave-api.com/v2/contracts/{token_id}"
    headers = {
        'X-API-KEY': api_key
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_and_save_risk_reports(json_path, api_key, output_path):
    token_ids = get_first_10_token_ids(json_path)
    results = []
    for token_id in token_ids:
        try:
            report = fetch_risk_report(token_id, api_key)
            results.append(report)
        except Exception as e:
            print(f"Error fetching {token_id}: {e}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def main():
    api_key = "HPmf6KfmMkNWWwcItyvPKHtv4BVCpM7gZU1JYsE7xwQcJqx41G6V5xKUdYCuMvvR"
    json_path = "tokenDatasets/searchToken.json"
    output_path = "tokenDatasets/getContractRiskDetectionReport.json"
    get_and_save_risk_reports(json_path, api_key, output_path)

if __name__ == "__main__":
    main()
