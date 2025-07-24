import requests
import json


def fetch_and_save_metadata(api_key: str, output_path: str, coin_id: str = "1"):
    """
    Fetches static metadata for one or more cryptocurrencies from CoinMarketCap v2 API and saves it to a JSON file.
    Args:
        api_key (str): Your CoinMarketCap API key.
        output_path (str): Path to save the resulting JSON data.
        coin_id (str): Comma-separated CoinMarketCap cryptocurrency IDs. Default is "1".
    """
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }
    params = {
        "id": coin_id,
        "aux": "urls,logo,description,tags,platform,date_added,notice,status"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    fetch_and_save_metadata(
        api_key="79570410-a0e3-4ca1-81f9-9c0626f0e31a",
        output_path="CoinMarket/coinMarketData/metadata.json",
        coin_id="1"
    )
