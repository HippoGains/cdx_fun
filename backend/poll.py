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
BINANCE_PAIRS_FILE = os.path.join(OUTPUT_DIR, 'binance_pairs.json')
import json
import requests


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


def fetch_binance_pairs():
    # Spot pairs
    spot_pairs = []
    try:
        exchange = ccxt.binance()
        markets = exchange.load_markets()
        spot_pairs = [symbol for symbol in markets if symbol.endswith('/USDT')]
    except Exception as e:
        print(f"Failed to fetch Binance spot pairs: {e}")

    # Futures pairs (using direct API for more reliability)
    futures_pairs = []
    try:
        url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        resp = requests.get(url, timeout=10)
        data = resp.json()
        for symbol in data['symbols']:
            if symbol['quoteAsset'] == 'USDT' and symbol['contractType'] in ['PERPETUAL', 'CURRENT_MONTH', 'NEXT_MONTH']:
                futures_pairs.append(symbol['symbol'])
    except Exception as e:
        print(f"Failed to fetch Binance futures pairs: {e}")

    return {
        'last_check': datetime.utcnow().isoformat(),
        'spot': spot_pairs,
        'futures': futures_pairs
    }

if __name__ == '__main__':
    ensure_output_dir()
    # Original price polling
    data = fetch_prices()
    if data:
        append_to_csv(data)
        print(f'Wrote {len(data)} rows to {CSV_FILE}')
    else:
        print('No data fetched')
    # New: fetch and save all Binance USDT pairs
    binance_pairs = fetch_binance_pairs()
    with open(BINANCE_PAIRS_FILE, 'w') as f:
        json.dump(binance_pairs, f, indent=2)
    print(f"Wrote Binance pairs to {BINANCE_PAIRS_FILE}")
