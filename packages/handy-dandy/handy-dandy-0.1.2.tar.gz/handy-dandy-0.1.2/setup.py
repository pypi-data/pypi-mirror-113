# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['handy_dandy']

package_data = \
{'': ['*']}

install_requires = \
['pyfiglet>=0.8.post1,<0.9']

setup_kwargs = {
    'name': 'handy-dandy',
    'version': '0.1.2',
    'description': 'A few handy tools for your python program!',
    'long_description': "# Handy Dandy\n*A collection of handy programs for your python project.*\n\n\n### Output validator\nHandy dandy's validate decorator can make sure that \nfunctions return the type that you want them to. \n\n```py\nfrom handy_dandy import validator as val\n\n@val.string # expecting function to return string\ndef foo(x):\n\treturn x\n\ny = foo(5)\n```\n\n\n## Timer\nRecords how long a function takes to run.\n```py\nfrom handy_dandy import timer\n\n@timer\ndef foo():\n\tpass\n```\n\n## System\nsystem function. Returns the computer's os (win32, win64, mac, linux).\n\n## Recorder\nRecords the amount of times it has been ran. This can be helpful when you want to see how many times multiple functions have been ran durring the program.\n\n```py\n>>> from handy_dandy import Recorder\n>>> x = Recorder('f', 's')\n>>> x.click('f')\n1\n>>> x.clicks()\n{'f': 1, 's': 0}\n>>> x.click()\n>>> x.clicks()\n{'f': 2, 's': 1}\n```\n\n## Design\nI made a bunch of text design programs for this package, inspired by [this](https://replit.com/talk/learn/Enhancing-Python-projects/142183). They're really self-explanitory, so i'll just give a list of the function names:\n- scroll_clear()\n- underline(text, color='white')\n- bold(text, color='white')\n- italic(text, color='white)\n- color(text, color)\n- ascii(text)",
    'author': 'Isaiah Day',
    'author_email': 'dont@stalk.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
