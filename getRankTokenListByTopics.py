import requests
import json

API_KEY = "SkSKVNdUY7SbvpE1ozuwxuZWn2RQlUMU0IAcGAOHCfTvDKkd4dYBc0nx4XKUwRvm"
API_URL = "https://prod.ave-api.com/v2/ranks"
OUTPUT_PATH = "tokenDatasets/getRankTokenListByTopics.json"

# 自定义 topic
TOPIC = "meme"  # 可根据需要更改
LIMIT = 10  # 可根据需要更改，最大300

headers = {
    "X-API-KEY": API_KEY
}
params = {
    "topic": TOPIC,
    "limit": LIMIT
}

response = requests.get(API_URL, headers=headers, params=params)

if response.status_code == 200:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=2)
    print(f"数据已保存到 {OUTPUT_PATH}")
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(response.text)
