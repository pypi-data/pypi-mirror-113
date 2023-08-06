from typing import Any, Dict, Optional

from yelpfusion.endpoint import Endpoint


class Events(Endpoint):
    def get(self, id: str, locale: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if locale:
            params["locale"] = locale

        return self._get(f"/events/{id}", params=params)

    def search(self, **params: Any) -> Dict[str, Any]:
        return self._get("/events", params=params)

    def featured(self, **params: Any) -> Dict[str, Any]:
        return self._get("/events/featured", params=params)
