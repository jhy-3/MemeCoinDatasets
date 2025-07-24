import requests
import json

def fetch_chain_trending_list(chain='solana', current_page=0, page_size=10, api_key='HPmf6KfmMkNWWwcItyvPKHtv4BVCpM7gZU1JYsE7xwQcJqx41G6V5xKUdYCuMvvR'):
    url = 'https://prod.ave-api.com/v2/tokens/trending'
    headers = {
        'X-API-KEY': api_key
    }
    params = {
        'chain': chain,
        'current_page': current_page,
        'page_size': page_size
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    with open('tokenDatasets/getChainTrendingList.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data

# Example usage:
# fetch_chain_trending_list()

def main():
    chain = 'solana'
    current_page = 0
    page_size = 10
    result = fetch_chain_trending_list(chain, current_page, page_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
