from typing import Any, Dict, Optional

from yelpfusion.endpoint import Endpoint


class Categories(Endpoint):
    def all(self, locale: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if locale:
            params["locale"] = locale

        return self._get("/categories", params=params)

    def details(self, alias: str, locale: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if locale:
            params["locale"] = locale

        return self._get(f"/categories/{alias}", params=params)
