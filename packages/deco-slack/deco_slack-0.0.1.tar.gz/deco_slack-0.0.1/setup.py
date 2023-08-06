# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deco_slack']

package_data = \
{'': ['*']}

install_requires = \
['slack-sdk>=3.3.1,<4.0.0']

entry_points = \
{'console_scripts': ['test = python -m pytest tests/ --verbose']}

setup_kwargs = {
    'name': 'deco-slack',
    'version': '0.0.1',
    'description': 'deco_slack notifies you if a method has completed successfully or not.',
    'long_description': '# decoslack\n\ndecoslack notifies you via Slack if a method has completed successfully or not.\n\n## Description\n\n- Notify Slack when a process starts, ends normally, or ends abnormally.\n- Each notification can be set on or off.\n\n## Configurations\nEnvironment variables to set\n- SLACK_TOKEN\n  - Slack bot token that can be used with chat:write.public scope.\n- SLACK_CHANNEL\n  - Channel name to be notified without # (like notify_xxx not #notify_xxx)\n\n## Example\n\n```py\nfrom deco_slack import deco_slack\n\n\n@deco_slack(\n    # These parameters are all optional\n    start={\n        "text": "start text",\n        "title": \'start\',\n        "color": "good"\n    },\n    success={\n        "text": "success text",\n        "title": \'success\',\n        "color": "good"\n    },\n    error={\n        "title": \'error\',\n        "color": "danger",\n        "stacktrace": True # Set True if you need stacktrace in a notification\n    },\n)\ndef test1():\n  print(\'test1\')\n\n\n@deco_slack(\n    success={\n        "text": "success text",\n        "title": \'success\',\n        "color": "good"\n    },\n    error={\n        "title": \'error\',\n        "color": "danger",\n        "stacktrace": True\n    },\n)\ndef error1():\n  raise ValueError(\'error occured.\')\n\n```\n',
    'author': 'taross-f',
    'author_email': 'taro.furuya@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/taross-f/deco-slack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
