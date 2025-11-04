"""
ConfigManager - Centralized configuration management
Separates public blockchain configs from private user secrets
"""

import os
import yaml
from typing import Dict, List, Optional
from pathlib import Path


class ConfigManager:
    """Manages loading and accessing configuration from multiple sources"""

    def __init__(
        self,
        chains_path: str = "chains.yaml",
        wallets_path: str = "wallets.yaml",
        assets_path: str = "assets.yaml"
    ):
        # Base path is the config directory where this file is located
        self.base_path = Path(__file__).parent
        self.chains = self._load_yaml(chains_path)
        self.wallets = self._load_yaml(wallets_path)
        self.assets = self._load_yaml(assets_path)
        self._validate_config()

    def _load_yaml(self, relative_path: str) -> dict:
        """Load YAML file with error handling"""
        try:
            # Handle both absolute and relative paths
            if Path(relative_path).is_absolute():
                file_path = Path(relative_path)
            else:
                file_path = self.base_path / relative_path

            with open(file_path, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"⚠️  Warning: {relative_path} not found at {file_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"❌ Error parsing {relative_path}: {e}")
            return {}

    def _validate_config(self):
        """Validate configuration on startup"""
        if not self.chains.get("chains"):
            raise ValueError("chains.yaml is missing or has no 'chains' section")

        if not self.wallets.get("wallets"):
            print("⚠️  Warning: No wallets configured in wallets.yaml")

    # === Chain Configuration Methods ===

    def get_chain_config(self, chain_name: str) -> Optional[Dict]:
        """Get full configuration for a blockchain"""
        return self.chains.get("chains", {}).get(chain_name)

    def get_all_chains(self) -> List[str]:
        """Get list of all configured chain names"""
        return list(self.chains.get("chains", {}).keys())

    def get_chain_id(self, chain_name: str) -> Optional[int]:
        """Get chain ID for a blockchain"""
        chain = self.get_chain_config(chain_name)
        return chain.get("chain_id") if chain else None

    def get_explorer_api(self, chain_name: str) -> Optional[str]:
        """Get explorer API URL for a blockchain"""
        chain = self.get_chain_config(chain_name)
        return chain.get("explorer_api") if chain else None

    def get_rpc_url(self, chain_name: str) -> Optional[str]:
        """Get RPC URL for a blockchain (with env var substitution)"""
        chain = self.get_chain_config(chain_name)
        if not chain:
            return None

        rpc_url = chain.get("rpc_url", "")
        # Replace {INFURA_API_KEY} with actual value from env
        if "{INFURA_API_KEY}" in rpc_url:
            infura_key = os.getenv("INFURA_API_KEY", "")
            rpc_url = rpc_url.replace("{INFURA_API_KEY}", infura_key)

        return rpc_url

    def get_native_token(self, chain_name: str) -> Optional[str]:
        """Get native token symbol for a blockchain"""
        chain = self.get_chain_config(chain_name)
        return chain.get("native_token") if chain else None

    def get_token_address(self, chain_name: str, token_symbol: str) -> Optional[str]:
        """Get contract address for a token on a specific chain"""
        chain = self.get_chain_config(chain_name)
        if not chain:
            return None

        tokens = chain.get("common_tokens", {})
        token_info = tokens.get(token_symbol)

        if isinstance(token_info, dict):
            return token_info.get("address")
        return token_info  # Legacy: direct address string

    def get_token_decimals(self, chain_name: str, token_symbol: str) -> int:
        """Get decimals for a token (with fallback to common defaults)"""
        chain = self.get_chain_config(chain_name)
        if not chain:
            return 18  # Default for most ERC-20 tokens

        # Check if token has explicit decimals in config
        tokens = chain.get("common_tokens", {})
        token_info = tokens.get(token_symbol)

        if isinstance(token_info, dict) and "decimals" in token_info:
            return token_info["decimals"]

        # Fallback to common decimals
        if token_symbol in ("USDT", "USDC"):
            return 6
        return 18

    # === Wallet Configuration Methods ===

    def get_user_addresses(self, chain_name: str) -> List[str]:
        """Get user's wallet addresses for a specific chain"""
        wallets = self.wallets.get("wallets", {})
        addresses = wallets.get(chain_name, [])

        # Support both list format and dict format (with labels)
        if isinstance(addresses, list):
            # Filter out None and empty strings
            return [addr for addr in addresses if addr]

        return []

    def get_all_wallet_chains(self) -> List[str]:
        """Get list of all chains where user has wallets configured"""
        return list(self.wallets.get("wallets", {}).keys())

    def has_wallets_for_chain(self, chain_name: str) -> bool:
        """Check if user has any wallets configured for a chain"""
        addresses = self.get_user_addresses(chain_name)
        return len(addresses) > 0

    # === Asset Configuration Methods ===

    def get_asset_info(self, symbol: str) -> Optional[Dict]:
        """Get asset information from assets.yaml"""
        assets = self.assets.get("assets", {})
        return assets.get(symbol)

    def get_coingecko_id(self, symbol: str) -> Optional[str]:
        """Get CoinGecko ID for a symbol"""
        asset = self.get_asset_info(symbol)
        return asset.get("coingecko_id") if asset else None

    # === Utility Methods ===

    def chain_exists(self, chain_name: str) -> bool:
        """Check if a chain is configured"""
        return chain_name in self.chains.get("chains", {})

    def get_supported_tokens(self, chain_name: str) -> List[str]:
        """Get list of all supported token symbols for a chain"""
        chain = self.get_chain_config(chain_name)
        if not chain:
            return []

        tokens = chain.get("common_tokens", {})
        return list(tokens.keys())


# Singleton instance
_config_manager_instance = None


def get_config_manager() -> ConfigManager:
    """Get singleton ConfigManager instance"""
    global _config_manager_instance
    if _config_manager_instance is None:
        _config_manager_instance = ConfigManager()
    return _config_manager_instance
