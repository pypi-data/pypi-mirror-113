from functools import lru_cache

from yelpfusion.endpoints.autocomplete import Autocomplete
from yelpfusion.endpoints.businesses import Businesses
from yelpfusion.endpoints.categories import Categories
from yelpfusion.endpoints.events import Events
from yelpfusion.endpoints.transactions import Transactions


class Api:
    def __init__(self, api_key: str):
        self.api_key = api_key

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def autocomplete(self) -> Autocomplete:
        return Autocomplete(self.api_key)

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def businesses(self) -> Businesses:
        return Businesses(self.api_key)

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def categories(self) -> Categories:
        return Categories(self.api_key)

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def events(self) -> Events:
        return Events(self.api_key)

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def transactions(self) -> Transactions:
        return Transactions(self.api_key)
