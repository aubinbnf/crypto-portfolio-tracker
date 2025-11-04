import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from connectors import Connector
from config.config_manager import ConfigManager

load_dotenv()


class EtherscanConnector(Connector):
    def __init__(self, config_manager: ConfigManager = None):
        """
        Initialize Etherscan connector with ConfigManager

        Args:
            config_manager: ConfigManager instance (creates new one if None)
        """
        self.config = config_manager or ConfigManager()
        self.api_key = os.getenv("ETHERSCAN_API_KEY")
        self.base_url = "https://api.etherscan.io/v2/api"

        if not self.api_key:
            raise ValueError("ETHERSCAN_API_KEY is missing from .env")

    def fetch_balances(self):
        """Retrieves balance for each address across all configured EVM chains"""
        all_balances = []

        # Iterate through all EVM chains (except bitcoin)
        for chain_name in self.config.get_all_wallet_chains():
            if chain_name == "bitcoin":
                continue  # Skip bitcoin, handled by BlockstreamConnector

            # Check if chain is configured
            if not self.config.chain_exists(chain_name):
                print(f"⚠️  Warning: Chain '{chain_name}' not found in chains.yaml")
                continue

            print(f"🔗 Fetching balances on {chain_name}...")

            chain_id = self.config.get_chain_id(chain_name)
            addresses = self.config.get_user_addresses(chain_name)

            # Get native token symbol
            native_token = self.config.get_native_token(chain_name)

            for address in addresses:
                # Fetch native token balance
                balance = self._get_native_balance(address, chain_name, chain_id, native_token)
                all_balances.append(balance)

                # Fetch common ERC-20 token balances
                supported_tokens = self.config.get_supported_tokens(chain_name)
                for token_symbol in supported_tokens:
                    token_address = self.config.get_token_address(chain_name, token_symbol)
                    balance = self._get_token_balances(
                        address, chain_name, chain_id, token_address, token_symbol
                    )
                    all_balances.append(balance)

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
        balance = 0
        if resp.get("status") == "1":
            raw_balance = int(resp.get("result", 0))
            decimals = self._guess_decimals(chain_name, symbol)
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

    def _guess_decimals(self, chain_name, symbol):
        """Get token decimals from config or use heuristics"""
        # Try to get from config first
        decimals = self.config.get_token_decimals(chain_name, symbol)
        if decimals:
            return decimals

        # Fallback to common defaults
        if symbol in ("USDT", "USDC"):
            return 6
        return 18