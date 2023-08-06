# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yelpfusion', 'yelpfusion.endpoints']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0']

setup_kwargs = {
    'name': 'yelpfusion',
    'version': '0.1.0',
    'description': 'A Python wrapper for Yelp Fusion API',
    'long_description': '# yelp-fusion-api\n\nA Python wrapper for Yelp Fusion API.\n\nPlease refer to the [API documentation](https://www.yelp.ca/developers/documentation/v3/get_started) for the details\nof expected requests and responses for all endpoints.\n\n## Installation\n\n`pip install -U yelpfusion`\n\n## Usage\n\n```python\nfrom yelpfusion import Api\n\napi = Api("api-token")\n\napi.businesses.search(location="Toronto")\n```\n\nThe available endpoints are:\n- Autocomplete: [api.autocomplete](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/autocomplete.py)\n- Businesses: [api.businesses](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/businesses.py)\n- Categories: [api.categories](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/categories.py)\n- Events: [api.events](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/events.py)\n- Transactions: [api.transactions](https://github.com/tmnhat2001/yelp-fusion-api/blob/main/yelpfusion/endpoints/transactions.py)\n',
    'author': 'James Tran',
    'author_email': 'tran.james2001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
