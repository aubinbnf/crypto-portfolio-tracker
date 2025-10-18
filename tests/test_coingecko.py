import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.connectors import CoinGeckoConnector

cg = CoinGeckoConnector()

token = "USDC"
token_id = "usd-coin"
blockchain = "arbitrum-one"
contract_address = cg.get_contract_addresses(token_id, blockchain)
print(f"token : {token}\ntoken id : {token_id}\nblockchain : {blockchain}\ncontract address : {contract_address}")