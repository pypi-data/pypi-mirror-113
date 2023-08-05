# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kodipydent']

package_data = \
{'': ['*']}

install_requires = \
['beekeeper-alt>=2021.7.16,<2022.0.0']

entry_points = \
{'poetry.application.plugin': ['plugin = '
                               'poetry_date_version_plugin.plugin:VersionPlugin']}

setup_kwargs = {
    'name': 'kodipydent-alt',
    'version': '2021.7.16',
    'description': 'A complete Python client for the Kodi JSON-RPC API',
    'long_description': 'kodipydent\n==========\nA complete Python client for the Kodi JSON-RPC API\n\n\nWhy?\n----\nBecause JSON-RPC is one of the trickier communication schemes to write for. And if you want to code for it, then you\'re probably going to get into bit of a dysfunctional relationship with the documentation. \n\nWhat?\n-----\nA native-Python JSON-RPC client. Loads all the methods from your Kodi instance each time it gets instantiated, so you know you\'re never behind. And, it puts it in some semblance of a reasonable object structure.\n\nFuture updates will bundle a carefully-manicured static hive that will give you a better object structure at the cost of not always being completely up-to-date.\n\nHow?\n----\n\n.. code:: python\n\n    >>> from kodipydent import Kodi\n    >>> my_kodi = Kodi(\'192.168.1.1\')\n    >>> movies = my_kodi.VideoLibrary.GetMovies()\n\nSimple as that. beekeeper makes it easy to use and easy to learn; if you don\'t know the name of the method you want to use, just do this:\n\n.. code:: python\n\n    >>> print(my_kodi)\n    \nand you\'ll get a printout of all the methods available, and all the variables each one takes.\n\nInstallation\n------------\n\n.. code:: bash\n\n    $ pip install kodipydent\n\nUnder the Hood\n--------------\n\nkodipydent is driven by beekeeper, the family-friendly, object-oriented Python REST library. With beekeeper, even JSON-RPC clients are relatively simple to write. Don\'t believe me? Read the code. And you can check out `kodipydent/hive.json` to see what a full hive looks like.\n\nHere\'s the full signature of the method to create your API:\n\n.. code:: python\n\n    Kodi(hostname[, port=8080, username=\'kodi\', password=None])\n\n"Advanced" Usage\n----------------\n\nkodipydent supports Kodi installations that have usernames and passwords set up. If you\'ve created a password for web access, then simply construct your kodipydent instance as follows:\n\n.. code:: python\n\n    Kodi(\'localhost\', username=\'kodi\', password=\'myawesomepassword\')\n',
    'author': 'Jesse Shapiro',
    'author_email': 'jesse@bedrockdata.com',
    'maintainer': 'Dustyn Gibson',
    'maintainer_email': 'miigotu@gmail.com',
    'url': 'https://github.com/miigotu/kodipydent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
