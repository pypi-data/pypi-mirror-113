# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fixtures',
 'fixtures.tests',
 'virtool_workflow',
 'virtool_workflow.analysis',
 'virtool_workflow.api',
 'virtool_workflow.caching',
 'virtool_workflow.data_model',
 'virtool_workflow.execution',
 'virtool_workflow.execution.hooks',
 'virtool_workflow.runtime',
 'virtool_workflow.storage',
 'virtool_workflow.testing']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'aiohttp>=3.7.3,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'virtool-core>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['workflow = virtool_workflow.cli:cli_main',
                     'workflow-test = integration_tests.cli:cli']}

setup_kwargs = {
    'name': 'virtool-workflow',
    'version': '0.6.0',
    'description': 'A framework for developing bioinformatics workflows for Virtool.',
    'long_description': '# Virtool Workflow\n\n![Tests](https://github.com/virtool/virtool-workflow/workflows/Tests/badge.svg?branch=master)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1bf01ed0b27040cc92b4ad2380e650d5)](https://www.codacy.com/gh/virtool/virtool-workflow/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=virtool/virtool-workflow&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/1bf01ed0b27040cc92b4ad2380e650d5)](https://www.codacy.com/gh/virtool/virtool-workflow/dashboard?utm_source=github.com&utm_medium=referral&utm_content=virtool/virtool-workflow&utm_campaign=Badge_Coverage)\n\nA framework for developing bioinformatic workflows in Python.\n\n```python\nfrom virtool_workflow import startup, step, cleanup\n\n@startup\ndef startup_function():\n    ...\n\n@step \ndef step_function():\n    ...\n\n@step\ndef step_function_2():\n    ...\n\n@cleanup\ndef cleanup_function():\n    ...\n```\n\n* [Documentation](https://workflow.virtool.ca)\n* [Virtool Website](https://www.virtool.ca/)\n* [PyPI Package](https://pypi.org/project/virtool-workflow/)\n',
    'author': 'Ian Boyes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/virtool/virtool-workflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
