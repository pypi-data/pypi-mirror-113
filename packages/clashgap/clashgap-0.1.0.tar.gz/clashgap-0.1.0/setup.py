# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clashgap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'clashgap',
    'version': '0.1.0',
    'description': 'A per-charecter diff/compression algorithm in python',
    'long_description': '## Clashgap\nA per-charecter diff/compression algorithm implementation in python\n\n### How it works\nIn case if you have two strings:\n> "This is a sentence..." and "This is a word..."\n\nyou could "clash" both of them together and find their gap, to get an array loking something like:\n> \\["This is a", \\["sentence", "word"\\], "..."\\]\n\nAs you can the clashgap algorithm looks for collisions in the two strings to find the gap\n\nThe clashgaped string maybe used for compression or as the diff of the input strings\n\n',
    'author': 'NioGreek',
    'author_email': 'GreekNio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/clashgap/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
