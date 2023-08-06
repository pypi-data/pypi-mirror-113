# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notion_renderer', 'notion_renderer.notion']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'bs4>=0.0.1,<0.0.2',
 'cached-property>=1.5.2,<2.0.0',
 'commonmark>=0.9.1,<0.10.0',
 'dictdiffer>=0.9.0,<0.10.0',
 'python-slugify>=5.0.2,<6.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.6.0,<11.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'tzlocal>=2.1,<3.0']

entry_points = \
{'console_scripts': ['notion_renderer = notion_renderer.__main__:app']}

setup_kwargs = {
    'name': 'notion-renderer',
    'version': '0.2.8',
    'description': 'Awesome `notion_renderer` is a Python cli/package created with https://github.com/TezRomacH/python-package-template',
    'long_description': '# notion_renderer\n',
    'author': 'notion_renderer',
    'author_email': 'ruucm.a@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/notion_renderer/notion_renderer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
