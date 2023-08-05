# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beekeeper']

package_data = \
{'': ['*']}

install_requires = \
['xmltodict>=0.9.2']

entry_points = \
{'poetry.application.plugin': ['plugin = '
                               'poetry_date_version_plugin.plugin:VersionPlugin']}

setup_kwargs = {
    'name': 'beekeeper-alt',
    'version': '2021.7.16',
    'description': 'beekeeper is a Python library designed around dynamically generating a RESTful client interface based on a minimal JSON hive',
    'long_description': 'beekeeper |Build Status| |Read Docs|\n====================================\n\nDescription\n-----------\n\nbeekeeper is a Python library designed around dynamically generating a\nRESTful client interface based on a minimal JSON hive.\n\nThe hive specification is designed to provide beekeeper (or other\napplications consuming hive files) with programmatically-designed\ninsight into the structure of both the REST endpoints that are available\nand the objects and methods that those endpoints represent.\n\nWhile the classes available in beekeeper can be used manually to create\nPythonic representations of REST endpoints, it is strongly preferred\nthat the library be used as a whole with a constructed hive file. As\nAPIs become larger in scale (in terms of the number of endpoints and\nrepresented objects), the time benefit of beekeeper becomes more\npronounced, as adding additional objects and endpoints is a trivial\nprocess.\n\nRequirements\n------------\n\nbeekeeper requires Python 2.7.9/3.4.3 or higher and their built-in\nmodules, as well as xmltodict.\n\nInstallation\n------------\n\n.. code:: python\n\n   pip install beekeeper\n\nUsage\n-----\n\nThe usage of beekeeper will depend on what features are provided by the\nperson who wrote the hive file. There are a number of ways that the hive\nwriter can make your life easier. Regardless, at a base level, usage will\nlook something like this:\n\n.. code:: python\n\n    from beekeeper import API\n    myAPI = API.from_hive_file(\'fname.json\')\n    x = myAPI.Widgets.action(id=\'foo\', argument=\'bar\')\n\nIf the hive developer defines an ID variable for the object you\'re working\nwith, you can subscript, dictionary style:\n\n.. code:: python\n\n    x = myAPI.Widgets[\'foo\'].action(argument=\'bar\')\n\nIf you\'ve only got one remaining argument in the method call, you don\'t even\nneed to name it! You can do something like this:\n\n.. code:: python\n\n   x = myAPI.Widgets[\'foo\'].action(\'bar\')\n\nThis also holds true if you have multiple variables, but the other ones are\nassigned by name:\n\n.. code:: python\n\n   x = myAPI.Widgets[\'foo\'].action(\'bar\', var2=\'baz\')\n\nIf you\'re using a hive file, then it should define which variables are needed.\nIf you try to call a function without filling in that variable, it should\nautomatically yell at you and tell you what variables are missing. Since these\nvariables are defined within the hive, beekeeper will do the work for you, \nautomatically determine what data type a particular variable is, and put it\nexactly where it needs to go.\n\nbeekeeper will also automatically handle parsing data. When you\nsend data, beekeeper will read the MIME type that was defined in the variable\nfor that data, and try to automatically move it from a "Python" format (e.g., \na dictionary) to the right REST API format (e.g., JSON).\n\nThis holds true in the other direction as well; beekeeper will read the MIME\ntype of the response data, and hand it back to you in a Pythonic format! If\nbeekeeper doesn\'t know how to handle the data, it\'ll just give you the raw\nbytes so that you can do what you need to with them.\n\nNotes\n-----\n\nbeekeeper does not currently do SSL certificate verification when used\non Python versions earlier than 2.7.9 or 3.4.3.\n\n.. |Build Status| image:: https://travis-ci.org/haikuginger/beekeeper.svg?branch=master\n   :target: https://travis-ci.org/haikuginger/beekeeper\n\n.. |Read Docs| image:: https://readthedocs.org/projects/beekeeper/badge/?version=latest\n    :target: http://beekeeper.readthedocs.org/en/latest/?badge=latest\n    :alt: Documentation Status',
    'author': 'Jesse Shapiro',
    'author_email': 'jesse@bedrockdata.com',
    'maintainer': 'Dustyn Gibson',
    'maintainer_email': 'miigotu@gmail.com',
    'url': 'https://github.com/miigotu/beekeeper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
