# yelp-fusion-api

A Python wrapper for Yelp Fusion API.

Please refer to the [API documentation](https://www.yelp.ca/developers/documentation/v3/get_started) for the details
of expected requests and responses for all endpoints.

## Installation

`pip install -U yelpfusion`

## Usage

```python
from yelpfusion import Api

api = Api("api-token")

api.businesses.search(location="Toronto")
```

The available endpoints are:
- Autocomplete: [api.autocomplete](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/autocomplete.py)
- Businesses: [api.businesses](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/businesses.py)
- Categories: [api.categories](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/categories.py)
- Events: [api.events](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/events.py)
- Transactions: [api.transactions](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/transactions.py)
