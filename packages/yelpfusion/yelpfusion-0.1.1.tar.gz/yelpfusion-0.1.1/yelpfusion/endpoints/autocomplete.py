from typing import Any, Dict

from yelpfusion.endpoint import Endpoint


class Autocomplete(Endpoint):
    def get(self, **params: Any) -> Dict[str, Any]:
        return self._get("/autocomplete", params=params)
