# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nino']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'nino',
    'version': '0.2.4',
    'description': 'A small unofficial AniList API wrapper made for python',
    'long_description': '# Basic examples\n\n# Character\n```py\nimport nino\nimport asyncio\n\n\nasync def test():\n    async with nino.Client() as client:\n        paginator = await client.character_search("Nino")\n        print(paginator.characters)\n\nasyncio.run(test())\n```\n\n# Anime\n```py\nimport nino\nimport asyncio\n\n\nasync def test():\n    async with nino.Client() as client:\n        paginator = await client.anime_search("Overlord", per_page=4)\n        for _ in range(4):\n            print(await paginator.next())\n\nasyncio.run(test())\n```\n\n# Documentation\n[Nino](https://an-dyy.github.io/nino/index.html)',
    'author': 'Andy',
    'author_email': 'yrisxl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/an-dyy/nino',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
