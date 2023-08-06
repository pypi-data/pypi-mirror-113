from typing import Any, Dict

from yelpfusion.endpoint import Endpoint


class Transactions(Endpoint):
    def search(self, transaction_type: str, **params: Any) -> Dict[str, Any]:
        return self._get(f"/transactions/{transaction_type}/search", params=params)
