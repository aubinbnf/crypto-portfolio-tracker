import os, requests, yaml
from dotenv import load_dotenv
from datetime import datetime
from connectors import Connector

load_dotenv()

class EtherscanConnector(Connector):
    def __init__(self, wallets_config="config/wallets.yaml", assets_path="config/assets.yaml"):
        self.api_key = os.getenv("ETHERSCAN_API_KEY")
        #self.addresses = [a.strip() for a in os.getenv("ETH_ADDRESSES", "").split(",") if a.strip()]
        self.base_url = "https://api.etherscan.io/v2/api"
        #if not self.api_key or not self.addresses:
        #    raise ValueError("ETHERSCAN_API_KEY or ETH_ADDRESSES is missing")
        
        with open(assets_path, "r") as f:
            self.assets_config = yaml.safe_load(f)

        with open(wallets_config, "r") as f:
            self.wallets_data = yaml.safe_load(f)["wallets"]
        #self.tokens = self.config.get("eth_tokens", {})

    def fetch_balances(self):
        """Retrieves balance for each address"""
        all_balances = []
        for chain_name, chain_conf in self.wallets_data.items():
            print(f"🔗 Fetching balances on {chain_name}...")

            chain_id = chain_conf["chain_id"]

            for addr_info in chain_conf["addresses"]:
                address = addr_info["address"]
                tokens = addr_info.get("tokens", [])
                for token in tokens:
                    for key, value in token.items():
                        if value == "native token": 
                            all_balances.append(self._get_native_balance(address, chain_name, chain_id, key))
                            print(all_balances)
                        else: 
                            all_balances.append(self._get_token_balances(address, chain_name, chain_id, value, key))

        return all_balances
    
    def _get_native_balance(self, address, chain_name, chain_id, symbol):
        """Retrieves native balance"""
        resp = self._request({
            "chainid": chain_id,
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest"
        })
        wei = int(resp.get("result", 0))
        eth = wei / 10**18
        return self._format_balance(chain_name, symbol, eth, address)

    def _get_token_balances(self, address, chain_name, chain_id, contract, symbol):
        """Retrieves ERC-20 balances for configured tokens"""
        resp = self._request({
            "chainid": chain_id,
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
        return self._format_balance(chain_name, symbol, balance, address)

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