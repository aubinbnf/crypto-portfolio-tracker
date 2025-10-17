import requests

class CoinGeckoConnector:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        pass

    def get_contract_addresses(self, token_id: str):
        """
        Returns a dict of contract addresses per blockchain for a given token_id.
        Example:
            get_contract_addresses("usd-coin")
            => {"ethereum": "0xA0b8...", "arbitrum-one": "0xaf88..."}
        """
        url = f"{self.BASE_URL}/coins/{token_id}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("platforms", {})

    def get_price(self, token_ids, vs="usd"):
        """
        Returns current prices for a list of token ids.
        Example:
            get_price(["usd-coin", "bitcoin"])
        """
        url = f"{self.BASE_URL}/simple/price"
        r = requests.get(url, params={"ids": ",".join(token_ids), "vs_currencies": vs}, timeout=10)
        r.raise_for_status()
        return r.json()