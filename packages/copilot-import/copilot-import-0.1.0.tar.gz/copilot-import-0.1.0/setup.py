# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['copilot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'copilot-import',
    'version': '0.1.0',
    'description': 'Inspired by https://github.com/drathier/stack-overflow-import',
    'long_description': '# Copilot Importer\n\nWhy write code when you can import it directly from GitHub Copilot?\n\n## What is Copilot Importer?\n\nThe `copilot` python module will dynamically generate any function imported\nby leveraging the GitHub Copilot service.\n\n## How do I use Copilot Importer?\n\nYou can install copilot-importer via pip (e.g. `pip install copilot-importer`).\n\nAdditionally and importantly, you need a GitHub Copilot API token. If you have\naccess to GitHub Copilot, you can find your token from (TODO: ADD TOKEN INSTRUCTIONS).\n\nOnce you have your token, set it to the environment variable\n`GITHUB_COPILOT_TOKEN`.\n\n```shell\nexport GITHUB_COPILOT_TOKEN=xxxxxxxxxxxxxxxxxxxx\n```\n\nFinally, before the dynamic importing feature is enabled, you must run the\n`copilot.install` method.\n\n```python\n# Enable copilot importer\nfrom copilot import install\ninstall()\n```\n\nAfter all of the above has been taken care of, you should be able to import\nanything you want directly from GitHub Copilot:\n\n```python\n>>> from copilot import install\n>>> install()\n\n>>> from copilot import base64_encode\n>>> base64_encode(b"test")\nb\'dGVzdA==\'\n\n>>> from copilot import base64_decode\n>>> base64_decode(base64_encode(b"test"))\nb\'test\'\n\n>>> from copilot import quicksort\n>>> quicksort([5,2,3,4])\n[2, 3, 4, 5]\n```\n\nYou can also output the code of imported functions like so:\n```python\n>>> from copilot import say_hello\n>>> print(say_hello._code)\ndef say_hello():\n    print("Hello, World!")\n```\n\n## Credits\n\n- Inspiration taken from\n  [stack-overflow-import](https://github.com/drathier/stack-overflow-import)\n- GitHub for providing GitHub Copilot\n- [molenzwiebel](https://github.com/molenzwiebel) for working out the copilot\n  API and most of the code\n- [akx](https://github.com/akx) for giving a quick review of the code\n',
    'author': 'Mythic',
    'author_email': 'mythicmaniac@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
