# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['citoolkit', 'citoolkit.improvisers', 'citoolkit.specifications']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'citoolkit',
    'version': '0.1.0',
    'description': 'A library containing tools to create and solve instances of the Control Improvisation problem and its extensions. Primarily maintained by Eric Vin <evin@ucsc.edu>',
    'long_description': None,
    'author': 'Eric Vin',
    'author_email': 'evin@ucsc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
