import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.services import Aggregator

agg = Aggregator()

balances = agg.get_all_balances()
print("=== Detailed balances ===")
for elem in balances:
    print(elem)

print("\n=== Totals per asset (with USD valuation) ===")
totals = agg.aggregate_by_asset(balances)
totals = agg.add_usd_values(totals)
total_amount_usd = 0
for t in totals:
    print(t)
    total_amount_usd += t["value_usd"]

print("\n=== Total amount in USD ===")
print(total_amount_usd)
