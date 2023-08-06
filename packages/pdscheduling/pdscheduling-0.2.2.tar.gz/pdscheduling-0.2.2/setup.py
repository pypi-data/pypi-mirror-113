# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdscheduling']

package_data = \
{'': ['*']}

install_requires = \
['pdpyras>=4.3.0,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pdscheduling',
    'version': '0.2.2',
    'description': '',
    'long_description': '# PDScheduling - a library to create schedules in PagerDuty\n\nJust generate an array with a user for every hour for the next week - and the library will push it to PagerDuty.\n\nInstall: `pip install pdscheduling`\n\n## Example:\n\n```python\nimport random\nfrom pdscheduling import PagerDuty\n\npd = PagerDuty("token")\nusers = pd.get_users()\nschedule = []\nfor day in range(7):\n    user = random.choice(users) # your fancy algorithm to select a user for the day\n    for hour in range(24): # btw, the week starts in UTC timezone\n        schedule += [user["id"]]\npd.create_or_update_schedule(name="Automatic Schedule", hours=schedule)\n```\n\n## Why library? Can I just use PagerDuty API?\n\nYou can, but it will be harder. PagerDuty don\'t give straightforward API for this, instead you need to create schedule\nwith a layer for every developer with proper restriction.\n\n## OptDuty\n\nThe library extracted from https://optduty.com. If you need a help with library or to create scheduling system please\nreach out roman@optduty.com\n',
    'author': 'Roman',
    'author_email': 'roman@optduty.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
