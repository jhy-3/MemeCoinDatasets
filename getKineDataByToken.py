import json
import requests
import time
from typing import List, Dict, Any

# API Configuration
API_KEY = "HPmf6KfmMkNWWwcItyvPKHtv4BVCpM7gZU1JYsE7xwQcJqx41G6V5xKUdYCuMvvR"
BASE_URL = "https://prod.ave-api.com/v2/klines/token"
CHAIN = "solana"
INTERVAL = 1
LIMIT = 30

def load_tokens_from_json(file_path: str) -> List[str]:
    """Load token IDs from the searchToken.json file."""
    tokens = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Skip the first line (header)
            next(file)
            
            for line in file:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        if 'token' in data:
                            tokens.append(data['token'])
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    return tokens

def get_kine_data(token_id: str) -> Dict[str, Any]:
    """Fetch Kine data for a specific token."""
    # Construct the token_id in the required format: {token}-{chain}
    full_token_id = f"{token_id}-{CHAIN}"
    
    # API endpoint
    url = f"{BASE_URL}/{full_token_id}"
    
    # Query parameters
    params = {
        'interval': INTERVAL,
        'limit': LIMIT
        # from_time and to_time are not specified (using defaults)
    }
    
    # Headers
    headers = {
        'X-API-KEY': API_KEY
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return {
            'token_id': full_token_id,
            'status': data.get('status'),
            'msg': data.get('msg'),
            'data': data.get('data', {})
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for token {token_id}: {e}")
        return {
            'token_id': full_token_id,
            'status': 0,
            'msg': f"Error: {str(e)}",
            'data': {}
        }
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON for token {token_id}: {e}")
        return {
            'token_id': full_token_id,
            'status': 0,
            'msg': f"JSON Parse Error: {str(e)}",
            'data': {}
        }

def main():
    """Main function to process all tokens and save results."""
    # Load tokens from the JSON file
    input_file = "tokenDatasets/searchToken.json"
    output_file = "tokenDatasets/getKineDataByToken.json"
    
    print("Loading tokens from searchToken.json...")
    tokens = load_tokens_from_json(input_file)
    
    if not tokens:
        print("No tokens found. Exiting.")
        return
    
    print(f"Found {len(tokens)} tokens. Starting to fetch Kine data...")
    
    # Store all results
    all_results = []
    
    # Process each token
    for i, token in enumerate(tokens, 1):
        print(f"Processing token {i}/{len(tokens)}: {token}")
        
        # Fetch Kine data
        result = get_kine_data(token)
        all_results.append(result)
        
        # Add a small delay to avoid overwhelming the API
        time.sleep(0.1)
    
    # Save results to JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(all_results, file, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_file}")
        print(f"Successfully processed {len(all_results)} tokens")
    except Exception as e:
        print(f"Error saving results: {e}")

if __name__ == "__main__":
    main()
