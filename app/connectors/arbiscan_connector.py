import os, requests, yaml
from dotenv import load_dotenv
from datetime import datetime
from app.connectors import Connector

load_dotenv()

class ArbiscanConnector(Connector):
    def __init__(self, config_path="app/config/assets.yaml"):
        self.api_key = os.getenv("ETHERSCAN_API_KEY")
        self.addresses = os.getenv("ETH_ADDRESSES", "").split(",")

        if not self.api_key or not self.addresses:
            raise ValueError("ETHERSCAN_API_KEY or ETH_ADDRESSES is missing")
        
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.tokens = self.config.get("eth_tokens", {})

    def fetch_balances(self):
        balances = []
        for address in self.addresses:
            address = address.strip()
            if not address:
                continue

            # ETH balance
            eth_resp = requests.get(
                "https://api.etherscan.io/v2/api?chainid=1",
                params={
                    "module": "account",
                    "action": "balance",
                    "address": address,
                    "tag": "latest",
                    "apikey": self.api_key
                },
                timeout=10
            )
            eth_resp.raise_for_status()
            data = eth_resp.json()
            wei = int(data["result"])
            eth = wei / 10**18

            balances.append({
                "source": "etherscan",
                "chain": "ethereum",
                "asset": "ETH",
                "balance": eth,
                "address": address,
                "fetched_at": datetime.utcnow().isoformat()
            })

            #ERC-20 token balances
            for symbol, contract in self.tokens.items():
                token_resp = requests.get(
                    "https://api.etherscan.io/v2/api?chainid=1",
                    params={
                        "module": "account",
                        "action": "tokenbalance",
                        "contractaddress": contract,
                        "address": address,
                        "tag": "latest",
                        "apikey": self.api_key
                    },
                    timeout=10
                )
                token_resp.raise_for_status()
                token_data = token_resp.json()
                if token_data.get("status") == "1":
                    raw_balance = int(token_data["result"])
                    decimals = 6 if symbol in ("USDT", "USDC") else 18
                    balance = raw_balance / (10 ** decimals)
                    
                    if balance > 0:
                        balances.append({
                            "source": "etherscan",
                            "chain": "ethereum",
                            "asset": symbol,
                            "balance": balance,
                            "address": address,
                            "fetched_at": datetime.utcnow().isoformat()
                        })            
        return balances