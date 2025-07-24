import requests
import json
import os

def extract_token_ids(txt_file):
    token_ids = []
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) < 3:
        return token_ids
    header = lines[0].strip().split('|')
    header = [h.strip() for h in header]
    token_idx = header.index('token')
    chain_idx = header.index('chain')
    for line in lines[2:]:
        cols = line.strip().split('|')
        if len(cols) <= max(token_idx, chain_idx):
            continue
        token = cols[token_idx].strip()
        chain = cols[chain_idx].strip()
        if token and chain:
            token_ids.append(f"{token}-{chain}")
    return token_ids

def get_token_prices(token_ids, api_key):
    if not api_key:
        raise ValueError('API KEY (X-API-KEY) is required!')
    url = 'https://prod.ave-api.com/v2/tokens/price'
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key
    }
    # API最多支持200个token_id
    all_results = {}
    for i in range(0, len(token_ids), 200):
        batch = token_ids[i:i+200]
        body = {'token_ids': batch}
        resp = requests.post(url, headers=headers, data=json.dumps(body))
        resp.raise_for_status()
        data = resp.json()
        # 合并data字段
        if 'data' in data:
            all_results.update(data['data'])
    # 构造最终返回格式
    result = {
        'status': 1,
        'msg': 'SUCCESS',
        'data_type': 1,
        'data': all_results
    }
    return result

def main():
    input_file = 'tokenDatasets/searchToken.txt'
    output_file = 'tokenDatasets/getTokenPrice.json'
    api_key = 'SkSKVNdUY7SbvpE1ozuwxuZWn2RQlUMU0IAcGAOHCfTvDKkd4dYBc0nx4XKUwRvm'  # 用户API KEY
    if not api_key:
        raise ValueError('请在getTokenPrice.py中填写你的API KEY (X-API-KEY)!')
    token_ids = extract_token_ids(input_file)
    if not token_ids:
        print('No token ids found.')
        return
    result = get_token_prices(token_ids, api_key=api_key)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f'Saved {len(result["data"])} token prices to {output_file}')

if __name__ == '__main__':
    main()
