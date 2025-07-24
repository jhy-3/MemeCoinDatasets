import requests
import json

def search_tokens(keyword, chain=None, limit=100, orderby=None):
    url = "https://prod.ave-api.com/v2/tokens"
    params = {
        "keyword": keyword,
        "limit": limit
    }
    if chain:
        params["chain"] = chain
    if orderby:
        params["orderby"] = orderby

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-API-KEY": "SkSKVNdUY7SbvpE1ozuwxuZWn2RQlUMU0IAcGAOHCfTvDKkd4dYBc0nx4XKUwRvm"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            tokens = data.get("data", [])
            for token in tokens:
                print(f"Name: {token.get('name')}")
                print(f"Symbol: {token.get('symbol')}")
                print(f"Chain: {token.get('chain')}")
                print(f"Current Price (USD): {token.get('current_price_usd')}")
                print(f"Market Cap: {token.get('market_cap')}")
                print(f"Logo URL: {token.get('logo_url')}")
                appendix = token.get('appendix')
                if appendix:
                    try:
                        appendix_json = json.loads(appendix)
                        print(f"Website: {appendix_json.get('website', '')}")
                    except Exception:
                        print(f"Appendix: {appendix}")
                print("-" * 40)
        else:
            print("API returned error:", data.get("msg"))
    else:
        print("HTTP error:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    search_tokens("TRUMP")
