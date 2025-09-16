from connectors.etherscan_connector import EtherscanConnector
from connectors.blockstream_connector import BlockstreamConnector
from connectors.binance_connector import BinanceConnector
from collections import defaultdict

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

balances = get_all_balances()
print("=== Detailed balances ===")
for elem in balances:
    print(elem)

print("\n=== Totals per asset ===")
totals = aggregate_by_asset(balances)
for t in totals:
    print(t)