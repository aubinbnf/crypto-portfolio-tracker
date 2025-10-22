import os, requests, yaml
from dotenv import load_dotenv
from datetime import datetime
from app.connectors import Connector

load_dotenv()

class EtherscanConnector(Connector):
    def __init__(self, config_path="app/config/assets.yaml"):
        self.api_key = os.getenv("ETHERSCAN_API_KEY")
        self.addresses = [a.strip() for a in os.getenv("ETH_ADDRESSES", "").split(",") if a.strip()]
        self.base_url = "https://api.etherscan.io/v2/api"
        if not self.api_key or not self.addresses:
            raise ValueError("ETHERSCAN_API_KEY or ETH_ADDRESSES is missing")
        
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.tokens = self.config.get("eth_tokens", {})

    def fetch_balances(self):
        """Retrieves the ETH + ERC20 balance for each address"""
        all_balances = []
        for address in self.addresses:
            eth_balance = self._get_native_balance(address)
            all_balances.append(eth_balance)

            token_balances = self._get_token_balances(address)
            all_balances.extend(token_balances)

        return all_balances
    
    def _get_native_balance(self, address):
        """Retrieves ETH balance"""
        resp = self._request({
            "chainid": 1,
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest"
        })
        wei = int(resp.get("result", 0))
        eth = wei / 10**18
        return self._format_balance("ethereum", "ETH", eth, address)

    def _get_token_balances(self, address):
        """Retrieves ERC-20 balances for configured tokens"""
        balances = []
        for symbol, contract in self.tokens.items():
            resp = self._request({
                "chainid": 1,
                "module": "account",
                "action": "tokenbalance",
                "contractaddress": contract,
                "address": address,
                "tag": "latest"
            })
            if resp.get("status") == "1":
                raw_balance = int(resp.get("result", 0))
                decimals = self._guess_decimals(symbol)
                balance = raw_balance / (10 ** decimals)
                if balance > 0:
                    balances.append(self._format_balance("ethereum", symbol, balance, address))
        return balances

    def _request(self, params):
        """Manages API calls to Etherscan"""
        params["apikey"] = self.api_key
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[EtherscanConnector] Request failed: {e}")
            return {}

    def _format_balance(self, chain, asset, balance, address):
        """Standardizes the structure of output data"""
        return {
            "source": "etherscan",
            "chain": chain,
            "asset": asset,
            "balance": balance,
            "address": address,
            "fetched_at": datetime.utcnow().isoformat()
        }

    def _guess_decimals(self, symbol):
        """Fast heuristics for token decimals"""
        if symbol in ("USDT", "USDC"):
            return 6
        return 18