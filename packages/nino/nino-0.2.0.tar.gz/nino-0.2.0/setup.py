# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nino']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'nino',
    'version': '0.2.0',
    'description': 'A small unofficial AniList API wrapper made for python',
    'long_description': '# Basic examples\n\n# Anime search\n```py\nfrom nino import Client\n\nwith Client() as client:\n    paginator = client.anime_search("Overlord")\n    print(paginator.animes)\n```\n\n# Character search\n```py\nfrom nino import Client\n\nwith Client() as client:\n    paginator = client.character_search("Nino")\n    print(paginator.characters)\n```',
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
