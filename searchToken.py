import os
import requests
import json

def search_tokens(keyword, chain=None, limit=100, api_key=None, output_file='tokenDatasets/searchToken.txt'):
    """
    搜索token信息，只保留描述性字段，字段名写在第一行，后续每行只输出这些字段的值，缺失则空字符串。所有列宽自动对齐，输出为纯文本表格格式。
    :param keyword: 搜索关键词（必填）
    :param chain: 区块链名称（可选）
    :param limit: 返回数量（默认100，最大300）
    :param api_key: API密钥（必填）
    :param output_file: 输出文件名（默认tokenDatasets/searchToken.txt）
    :return: None
    """
    if not keyword or not api_key:
        raise ValueError('keyword和api_key为必填项')
    url = 'https://prod.ave-api.com/v2/tokens'
    headers = {
        'X-API-KEY': api_key
    }
    params = {
        'keyword': keyword,
        'limit': limit
    }
    if chain:
        params['chain'] = chain
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    tokens = data.get('data', [])
    # 只保留描述性字段
    fields = [
        'total', 'launch_price', 'current_price_eth', 'current_price_usd', 'price_change_1d', 'price_change_24h',
        'lock_amount', 'burn_amount', 'tx_amount_24h', 'tx_volume_u_24h', 'locked_percent', 'market_cap', 'fdv',
        'tvl', 'main_pair_tvl', 'token', 'chain', 'decimal', 'name', 'symbol', 'holders', 'logo_url', 'risk_score',
        'launch_at', 'created_at', 'tx_count_24h', 'lock_platform', 'is_mintable', 'updated_at', 'main_pair'
    ]
    # 计算每列最大宽度
    col_widths = [len(f) for f in fields]
    rows = []
    for token in tokens:
        row = []
        for i, f in enumerate(fields):
            val = token.get(f, "")
            val_str = str(val) if val is not None else ""
            row.append(val_str)
            if len(val_str) > col_widths[i]:
                col_widths[i] = len(val_str)
        rows.append(row)
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # 写入表格
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写字段名
        header = ' | '.join(f.ljust(col_widths[i]) for i, f in enumerate(fields))
        f.write(header + '\n')
        f.write('-+-'.join('-' * w for w in col_widths) + '\n')
        # 写每行数据
        for row in rows:
            line = ' | '.join(row[i].ljust(col_widths[i]) for i in range(len(fields)))
            f.write(line + '\n')

if __name__ == '__main__':
    api_key = 'SkSKVNdUY7SbvpE1ozuwxuZWn2RQlUMU0IAcGAOHCfTvDKkd4dYBc0nx4XKUwRvm'
    search_tokens(
        keyword='trump',
        chain='solana',
        limit=100,
        api_key=api_key,
        output_file='tokenDatasets/searchToken.txt'
    )
