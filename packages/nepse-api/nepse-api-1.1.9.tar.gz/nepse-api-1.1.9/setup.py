# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nepse', 'nepse.broker', 'nepse.market', 'nepse.security']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'cachetools>=4.2.2,<5.0.0',
 'httpx>=0.18.1,<0.19.0',
 'pyhumps>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'nepse-api',
    'version': '1.1.9',
    'description': 'This is a API wrapper for NEPSE API.',
    'long_description': '# NEPSE API Wrapper\n\nThis python module fetches the data from [Nepali Stock Site](https://newweb.nepalstock.com/) and provides them in a pythonic\nand usable way.\n\n\n## About\n\nThis is a API wrapper for NEPSE API. This project was inspired from [PyPi Nepse](https://github.com/pyFrappe/nepse). \n\n## Documentation\n\nThere is a detailed guide in my documentation page for getting started and installing.\n[Documentation](https://nepse-api.readthedocs.io/)\n\n## How to use?\n\nYou can use this by package from [Nepse API PyPi](https://pypi.org/project/nepse-api/)\n```sh\npip install nepse-api\n```\n\n## Why use this?\n\nHow is this better than [PyPi Nepse](https://github.com/pyFrappe/nepse)?\n- It is asynchronous.\n- Data can be taken as attributes rather than from dict.\n- Data is fetched from the API rather than scraping the site.\n- Data is cached \n\n## APIs used\n\nThe APIs that I used to create this API wrapper is:\n- https://newweb.nepalstock.com/api/\n\n## How to use?\n\n```py\nimport asyncio\nimport httpx\nfrom nepse import Client\n\n\nasync def main():\n    company_Symbol = input(\'Input Company Symbol (Uppercase): \')\n\n    # Doing this is optional you can directly\n    # Initialize using `client = Client()` as well\n    async with httpx.AsyncClient() as async_client:\n        # Initializes the client\n        client = Client(httpx_client=async_client)\n\n        # Gets the data\n        data = await client.security_client.get_company(symbol=f"{company_Symbol}")\n\n        # Prints the highest price for that company today\n        print(f\'High Price of {company_Symbol}: \', data.high_price)\n        print(f\'Low price of {company_Symbol}: \', data.low_price)\n        print(f\'Open Price of {company_Symbol}: \', data.open_price)\n\n# Run the function\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n\n## Why are the attributes so in-costistent?\n\nThe attribues are in-consistent because the attributes are set according to the response set by the API. \nI tried changing it up but that would be distruptive because the comability with the API would be broken. \n\n## Want To Contribute?\n\nYou can send a pull request or open an issue to contribute.\nCheck out [Code Of Conduct](CODE_OF_CONDUCT.md) before contributing.\n',
    'author': 'Samrid Pandit',
    'author_email': 'samrid.pandit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Samrid-Pandit/nepse-api/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
