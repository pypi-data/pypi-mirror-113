# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raider']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'hy>=0.20.0,<0.21.0',
 'importlib-metadata>=4.6.1,<5.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'raider',
    'version': '0.1.3',
    'description': 'Authentication testing tool',
    'long_description': "# What is this\n\nThis is a tool designed to test authentication for web\napplications. While web proxies like\n[ZAProxy](https://www.zaproxy.org/) and\n[Burpsuite](https://portswigger.net/burp) allow authenticated tests,\nthey don't provide features to test the authentication process itself,\ni.e. manipulating the relevant input fields to identify broken\nauthentication. Most authentication bugs in the wild have been found\nby manually testing it or writing custom scripts that replicate the\nbehaviour. **Raider** aims to make testing easier, by providing the\ninterface to interact with all important elements found in modern\nauthentication systems.\n\n# Features\n\n**Raider** has the goal to support most of the modern authentication\nsystems, and for now it has the following features:\n\n* Unlimited authentication steps\n* Unlimited inputs/outputs for each step\n* Running arbitrary operations when receiving the response\n* Testing under multiple users\n* Writing custom operations and plugins\n\n\n# How does it work\n\n**Raider** treats the authentication as a finite state machine. Each\nauthentication step is a different state, with its own inputs and\noutputs. Those can be cookies, headers, CSRF tokens, or other pieces\nof information.\n\nEach application needs its own configuration file for **Raider** to\nwork. The configuration is written in\n[Hylang](https://docs.hylang.org/). The language choice was done for\nmultiple reasons, mainly because it's a Lisp dialect embedded in\nPython.\n\nUsing Lisp was necessarily since sometimes the authentication can get\nquite complex, and using a static configuration file would've not been\nenough to cover all the details. Lisp makes it easy to combine code\nand data, which is exactly what was needed here.\n\nBy using a real programming language as a configuration file gives\n**Raider** a lot of power, and with great power comes great\nresponsibility. Theoretically one can write entire malware inside the\napplication configuration file, which means you should be careful\nwhat's being executed, and **not to use configuration files from\nsources you don't trust**. **Raider** will evaluate everything inside\nthe .hy files, which means if you're not careful you could shoot\nyourself in the foot and break something on your system.\n\n# Installation\n\n**Raider** is available on PyPi:\n\n```\n$ pip3 install --user raider\n```\n\n# The Documentation is available on [Read the Docs](https://raider.readthedocs.io/en/latest/).\n",
    'author': 'Daniel Neagaru',
    'author_email': 'daniel@digeex.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
