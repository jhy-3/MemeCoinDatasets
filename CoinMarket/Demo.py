from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os

def fetch_and_save_crypto_data(parameters, output_path):
    """
    Fetch crypto data from CoinMarketCap API with given parameters and save as pretty JSON.
    Args:
        parameters (dict): Parameters for the API request.
        output_path (str): Path to save the resulting JSON file.
    Returns:
        dict: The fetched data.
    """
    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '79570410-a0e3-4ca1-81f9-9c0626f0e31a',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = response.json()
        # 自动整理格式并优雅输出
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise RuntimeError(f"Error fetching crypto data: {e}")

# 示例用法（可注释掉）
if __name__ == "__main__":
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    output_path = os.path.join(os.path.dirname(__file__), 'coinMarketData', 'getCrypto.json')
    fetch_and_save_crypto_data(parameters, output_path)
  