from typing import List

import requests


class WalletHandler:
    def __init__(self, api_key: str, *args, **kwargs):
        self.__api_key = api_key

    def _get_basic_info_of_wallet(self, chain_name: str, wallet_address: str):
        url_params = {}
        headers = {
            "Authorization": f"Bearer {str(self.__api_key)}",
            "X-Requested-With": "com.covalenthq.sdk.python/1.0.2",
            "quote-currency": "USD",
            "no-nft-asset-metadata": str(True),
        }
        url = f"https://api.covalenthq.com/v1/{chain_name}/address/{wallet_address}/balances_v2/"

        try:
            response = requests.get(
                url,
                params=url_params,
                headers=headers,
            )
            data = response.json()
        except Exception as ex:
            data = None

        return data

    def get_all_assets_of_wallet_address(self, *args, **kwargs) -> List:
        data = self._get_basic_info_of_wallet(*args, **kwargs)

        assets: List = data.get("data", {}).get("items", None)

        return assets

    def get_sum_balance_of_wallet_address(self, *args, **kwargs):
        assets: List = self.get_all_assets_of_wallet_address(*args, **kwargs)

        def string_to_float(price_str: str) -> float:
            return float(price_str.replace('$', ''))

        has_pretty_quotes = filter(lambda asset: asset.get('pretty_quote', None), assets)
        pretty_quotes = map(lambda asset: string_to_float(asset.get('pretty_quote', None)), has_pretty_quotes)
        balance_sum: float = sum(pretty_quotes)

        return balance_sum

    def _get_transactions_of_wallet_address(self, chain_name: str, wallet_address: str, page: int = 0):
        url_params = {}
        headers = {
            "Authorization": f"Bearer {str(self.__api_key)}",
            "accept": "application/json",
            # "X-Requested-With": "com.covalenthq.sdk.python/1.0.2",
            # "quote-currency": "USD",
            # "no-nft-asset-metadata": str(True),
        }
        url = f"https://api.covalenthq.com/v1/{chain_name}/address/{wallet_address}/transactions_v3/page/{page}/"

        try:
            response = requests.get(
                url,
                params=url_params,
                headers=headers,
            )
            data = response.json()
        except Exception as ex:
            data = None

        return data

    def get_transactions_with_paging(self, *args, **kwargs):
        data = self._get_transactions_of_wallet_address(*args, **kwargs)

        current_transactions: List = data.get("data", {}).get("items", None)

        return current_transactions

