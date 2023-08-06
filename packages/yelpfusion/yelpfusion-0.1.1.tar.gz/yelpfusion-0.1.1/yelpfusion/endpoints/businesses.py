from typing import Any, Dict, Optional

from yelpfusion.endpoint import Endpoint


class Businesses(Endpoint):
    def search(self, **params: Any) -> Dict[str, Any]:
        return self._get("/businesses/search", params)

    def search_by_phone_number(self, phone: str, locale: Optional[str] = None) -> Dict[str, Any]:
        params = {"phone": phone}
        if locale:
            params["locale"] = locale

        return self._get("/businesses/search/phone", params=params)

    def details(self, business_id: str, locale: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if locale:
            params["locale"] = locale

        return self._get(f"/businesses/{business_id}", params=params)

    def matches(self, **params: Any) -> Dict[str, Any]:
        return self._get("/businesses/matches", params=params)

    def reviews(self, business_id: str, locale: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if locale:
            params["locale"] = locale

        return self._get(f"/businesses/{business_id}/reviews", params=params)
