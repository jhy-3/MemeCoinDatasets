import requests
import time
import json

def search_tokens(keyword, chain="solana", limit=10):
    url = "https://prod.ave-api.com/v2/tokens"
    params = {
        "keyword": keyword,
        "chain": chain,
        "limit": limit
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != 1:
        raise Exception(f"API返回异常: {data.get('msg')}")
    return data.get("data", [])

def main():
    keyword = "meme"
    tokens = search_tokens(keyword)
    result = {
        "timestamp": int(time.time()),
        "meta": {
            "source": "prod.ave-api.com",
            "chain": "solana",
            "keyword": keyword,
            "count": len(tokens)
        },
        "tokens": []
    }
    for token in tokens:
        token_info = {
            "name": token.get("name"),
            "symbol": token.get("symbol"),
            "address": token.get("token"),
            "image": token.get("logo_url"),
            "launch_price": token.get("launch_price"),
            "current_price_usd": token.get("current_price_usd"),
            "market_cap": token.get("market_cap"),
            "holders": token.get("holders"),
            "created_at": token.get("created_at"),
            "appendix": token.get("appendix"),
        }
        result["tokens"].append(token_info)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
