#!/usr/bin/env python3
import csv
import os
from datetime import datetime

import pandas as pd
import ccxt

# Configuration
EXCHANGES = [
    ('binance', 'BTC/USDT'),
    ('kraken', 'BTC/USDT'),
    ('coinbase', 'BTC/USD'),
]
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CSV_FILE = os.path.join(OUTPUT_DIR, 'prices.csv')


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_prices():
    rows = []
    ts = datetime.utcnow().isoformat()
    for exch_id, symbol in EXCHANGES:
        try:
            exchange_class = getattr(ccxt, exch_id)
            exchange = exchange_class()
            ticker = exchange.fetch_ticker(symbol)
            price = ticker['last']
            rows.append({'timestamp': ts, 'exchange': exch_id, 'symbol': symbol, 'price': price})
        except Exception as e:
            print(f"Failed to fetch {symbol} from {exch_id}: {e}")
    return rows


def append_to_csv(rows):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'exchange', 'symbol', 'price'])
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    ensure_output_dir()
    data = fetch_prices()
    if data:
        append_to_csv(data)
        print(f'Wrote {len(data)} rows to {CSV_FILE}')
    else:
        print('No data fetched')
