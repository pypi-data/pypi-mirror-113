# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['how_short']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'how-short',
    'version': '0.1.1',
    'description': 'A simple decorator to measure a function excecution time. Clone of https://pypi.org/project/how-long/.',
    'long_description': 'how_short\n=========\n\nSimple Decorator to measure a function execution time.\nClone of `how-long <https://pypi.org/project/how-long/>`_.\n\nExample\n_______\n\n.. code-block:: python\n\n    from how_long import timer\n\n\n    @timer\n    def some_function():\n        return [x for x in range(10_000_000)]',
    'author': 'Aleksey Semenov',
    'author_email': 'alexsemenov1610@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/borgishmorg/how-short',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
