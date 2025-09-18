import requests
from connectors.etherscan_connector import EtherscanConnector
from connectors.blockstream_connector import BlockstreamConnector
from connectors.binance_connector import BinanceConnector
from collections import defaultdict

ASSET_TO_COINGECKO = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "BNB": "binancecoin",
    "ADA": "cardano",
    "SOL": "solana",
    "ETC": "ethereum-classic",
    "USDC": "usd-coin", 
    "DOT": "polkadot",
    "EGLD": "elrond-erd-2",
    "GRT": "the-graph",
    "ETHW": "ethereum-pow-iou"
}

def get_all_balances():
    connectors = [
        EtherscanConnector(),
        BlockstreamConnector(),
        BinanceConnector()
    ]
    balances = []
    for c in connectors:
        result = c.fetch_balances()
        balances.extend(result if isinstance(result, list) else [result])
    return balances

def aggregate_by_asset(balances):
    totals = defaultdict(float)

    for b in balances:
        asset = b["asset"]
        totals[asset] += b["balance"]

    return [{"asset": asset, "total_balance": balance} for asset, balance in totals.items()]

def fetch_prices(assets, vs="usd"):
    ids = [ASSET_TO_COINGECKO[a] for a in assets if a in ASSET_TO_COINGECKO]
    url = "https://api.coingecko.com/api/v3/simple/price"
    r = requests.get(url, params={"ids": ",".join(ids), "vs_currencies": vs}, timeout=10)
    r.raise_for_status()
    return r.json()

def add_usd_values(totals):
    assets = [t["asset"] for t in totals]
    prices = fetch_prices(assets)
    for t in totals:
        asset = t["asset"]
        cg_id = ASSET_TO_COINGECKO.get(asset)
        if cg_id and cg_id in prices:
            price = prices[cg_id]["usd"]
            t["price_usd"] = price
            t["value_usd"] = t["total_balance"] * price
        else:
            t["price_usd"] = None
            t["value_usd"] = None
    return totals

balances = get_all_balances()
print("=== Detailed balances ===")
for elem in balances:
    print(elem)

print("\n=== Totals per asset (with USD valuation) ===")
totals = aggregate_by_asset(balances)
totals = add_usd_values(totals)
total_amount_usd = 0
for t in totals:
    print(t)
    total_amount_usd += t["value_usd"]

print("\n=== Total amount in USD ===")
print(total_amount_usd)
