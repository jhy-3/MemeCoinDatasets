import requests
import json
import os

# CoinMarketCap API endpoint
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"

# 请求头，填入你的API Key
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "79570410-a0e3-4ca1-81f9-9c0626f0e31a",  # 替换为你的API Key
}

# 可选参数
params = {
    "listing_status": "active",  # 只获取活跃币种
    "sort": "id",
    "limit": 5000,  # 最大5000条
    "aux": "platform,first_historical_data,last_historical_data,is_active"
}

# 发起GET请求
response = requests.get(url, headers=headers, params=params)
data = response.json()

# 保存路径
save_path = os.path.join("CoinMarket", "coinMarketData", "coinMarketID.json")

# 保存为json文件
with open(save_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"数据已保存到 {save_path}")
