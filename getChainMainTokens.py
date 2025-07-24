import requests
import json

def fetch_chain_main_tokens(chain_name="solana"):
    """
    Fetch main tokens for a given chain from the API and save the response to tokenDatasets/getChainMainTokens.json.
    """
    url = f"https://prod.ave-api.com/v2/tokens/main?chain={chain_name}"
    headers = {
        "X-API-KEY": "HPmf6KfmMkNWWwcItyvPKHtv4BVCpM7gZU1JYsE7xwQcJqx41G6V5xKUdYCuMvvR"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()
    with open("tokenDatasets/getChainMainTokens.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data

if __name__ == "__main__":
    fetch_chain_main_tokens()
