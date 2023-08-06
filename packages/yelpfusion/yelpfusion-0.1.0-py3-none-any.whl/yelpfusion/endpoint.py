from typing import Any, Dict

import requests

BASE_URL = "https://api.yelp.com/v3"


class Endpoint:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.get(f"{BASE_URL}{path}", params=params, headers=self._request_header())
        response.raise_for_status()

        return response.json()

    def _request_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}
