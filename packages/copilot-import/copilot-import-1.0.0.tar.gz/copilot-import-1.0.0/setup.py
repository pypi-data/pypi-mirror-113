# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['copilot']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['copilot-auth = copilot.authflow:run']}

setup_kwargs = {
    'name': 'copilot-import',
    'version': '1.0.0',
    'description': 'Inspired by https://github.com/drathier/stack-overflow-import',
    'long_description': '# Copilot Importer\n\nWhy write code when you can import it directly from GitHub Copilot?\n\n## What is Copilot Importer?\n\nThe `copilot` python module will dynamically generate any function imported\nby leveraging the GitHub Copilot service.\n\n## How do I use Copilot Importer?\n\nYou can install copilot-importer via pip (e.g. `pip install copilot-importer`).\n\nAdditionally and importantly, you need a GitHub Copilot API token. See\n[How do I get an authentication token](#how-do-I-get-an-authentication-token).\n\nOnce you have your token, set it to the environment variable\n`GITHUB_COPILOT_TOKEN`.\n\n```shell\nexport GITHUB_COPILOT_TOKEN=xxxxxxxxxxxxxxxxxxxx\n```\n\nFinally, before the dynamic importing feature is enabled, you must run the\n`copilot.install` method.\n\n```python\n# Enable copilot importer\nfrom copilot import install\ninstall()\n```\n\nAfter all of the above has been taken care of, you should be able to import\nanything you want directly from GitHub Copilot:\n\n```python\n>>> from copilot import install\n>>> install()\n\n>>> from copilot import base64_encode\n>>> base64_encode(b"test")\nb\'dGVzdA==\'\n\n>>> from copilot import base64_decode\n>>> base64_decode(base64_encode(b"test"))\nb\'test\'\n\n>>> from copilot import quicksort\n>>> quicksort([5,2,3,4])\n[2, 3, 4, 5]\n```\n\nYou can also output the code of imported functions like so:\n```python\n>>> from copilot import say_hello\n>>> print(say_hello._code)\ndef say_hello():\n    print("Hello, World!")\n```\n\n## How do I get an authentication token?\n\nTo obtain an authentication token to the Copilot API, you will need a GitHub\naccount with access to Copilot.\n\n`copilot-importer` has an authentication CLI built-in, which you can use to\nfetch your copilot authentication token. To star the authentication process\nafter installing `copilot-importer`, simply run\n```shell\ncopilot-auth\n```\nOR\n```shell\npython -m copilot\n```\nOR\n```shell\npython -c "from copilot.authflow import run; run()"\n```\n\nOnce you have started the authentication flow, you will be prompted to enter\na device authorization code to\n[https://github.com/login/device](https://github.com/login/device).\n\nAfter entering the correct code, you will be asked to authorize\n_GitHub for VSCode_ to access your account. This is expected, as the Copilot\nAPI is only accessible to the VSCode plugin.\n\nOnce approved, you should see a Copilot access token printed to the terminal.\n\nExample:\n```console\n$ copilot-auth\nInitializing a login session...\nYOUR DEVICE AUTHORIZATION CODE IS: XXXX-XXXX\nInput the code to https://github.com/login/device in order to authenticate.\n\nPolling for login session status until 2021-07-17T17:26:01.618386\nPolling for login session status: authorization_pending\nPolling for login session status: authorization_pending\nSuccessfully obtained copilot token!\n\n\nYOUR TOKEN: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\nEXPIRES AT: 2021-07-17T21:21:39\n\nYou can add the token to your environment e.g. with\nexport GITHUB_COPILOT_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n```\n\n\n## Credits\n\n- Inspiration taken from\n  [stack-overflow-import](https://github.com/drathier/stack-overflow-import)\n- GitHub for providing GitHub Copilot.\n- [molenzwiebel](https://github.com/molenzwiebel) for working out the Copilot\n  API and helping with the code.\n- [akx](https://github.com/akx) for giving a quick review of the code.\n',
    'author': 'Mythic',
    'author_email': 'mythicmaniac@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MythicManiac/copilot-import',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
