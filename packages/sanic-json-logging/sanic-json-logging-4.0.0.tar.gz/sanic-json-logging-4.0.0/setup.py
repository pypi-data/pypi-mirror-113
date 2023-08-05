# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sanic_json_logging']

package_data = \
{'': ['*']}

install_requires = \
['sanic>=21.6.0']

setup_kwargs = {
    'name': 'sanic-json-logging',
    'version': '4.0.0',
    'description': 'Simple library to emit json formatted logs to stdout',
    'long_description': '==================\nsanic-json-logging\n==================\n\n.. image:: https://img.shields.io/pypi/v/sanic-json-logging.svg\n        :target: https://pypi.python.org/pypi/sanic-json-logging\n\n.. image:: https://travis-ci.com/terrycain/sanic-json-logging.svg?branch=master\n        :target: https://travis-ci.com/terrycain/sanic-json-logging\n\n.. image:: https://codecov.io/gh/terrycain/sanic-json-logging/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/terrycain/sanic-json-logging\n        :alt: Code coverage\n\n.. image:: https://pyup.io/repos/github/terrycain/sanic-json-logging/shield.svg\n     :target: https://pyup.io/repos/github/terrycain/sanic-json-logging/\n     :alt: Updates\n\nThe other day I was running some containers on Amazon\'s ECS and logging to cloudwatch. I then learnt cloudwatch parses JSON logs so\nobviously I then wanted Sanic to log out JSON.\n\nIdeally this\'ll be useful to people but if it isn\'t, raise an issue and we\'ll make it better :)\n\nTo install:\n\n.. code-block:: bash\n\n    pip install sanic-json-logging\n\nLook at ``examples/simple.py`` for a full working example, but this will essentially get you going\n\n.. code-block:: python\n\n    import sanic\n    from sanic_json_logging import setup_json_logging\n\n    app = sanic.Sanic()\n    setup_json_logging(app)\n\n\n``setup_json_logging`` does the following:\n\n- changes the default log formatters to JSON ones\n- also filters out no Keepalive warnings\n- unless told otherwise, will change the asyncio task factory, to implement some rudimentary task-local storage.\n- installs pre and post request middleware. Pre-request middleware to time tasks and generate a uuid4 request id. Post-request middleware to emit access logs.\n- will use AWS X-Forwarded-For IPs in the access logs if present\n\nIf ``setup_json_logging`` changed the task factory, all tasks created from the request\'s task will contain the request ID.\nYou can pass ``disable_json_access_log=True`` to the setup function which will disable the configuration of JSON access logging.\nSetting ``configure_task_local_storage`` to false will disable storing request IDs inside the task object which will\n\nCurrently I have it outputting access logs like\n\n.. code-block:: json\n\n    {\n      "timestamp": "2018-06-09T17:42:52.195701Z",\n      "level": "INFO",\n      "method": "GET",\n      "path": "/endpoint1",\n      "remote": "127.0.0.1:33468",\n      "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",\n      "host": "localhost:8000",\n      "response_time": 0.0,\n      "req_id": "795617c7-b514-4ed9-bb63-cc4fcd883c3d",\n      "logger": "sanic.access",\n      "status_code": 200,\n      "length": 0,\n      "type": "access"\n    }\n\nAnd if you log to the ``root`` logger, inside a request, it\'ll look like this.\n\n.. code-block:: json\n\n    {\n      "timestamp": "2018-06-09T17:42:52.195326Z",\n      "level": "INFO",\n      "message": "some informational message",\n      "type": "log",\n      "logger": "root",\n      "filename": "simple.py",\n      "lineno": 16,\n      "req_id": "795617c7-b514-4ed9-bb63-cc4fcd883c3d"\n    }\n\nChangelog\n---------\n\n4.0.0\n=====\n* Added flake8, black, isort, mypy\n* Dropped Travis in favour of Github Actions\n* Switched from setup.py to using Poetry\n* Updated tests to use ``sanic-testing``\n\n3.2.0\n=====\n* Updated to use new ``request.ctx`` context dictionary\n* Added support for Python 3.7 asyncio changes\n\n3.1.0\n=====\n* Stringify any LogRecord message if its not JSON serializable\n\n3.0.0\n=====\n* Added option to disable task local storage\n\n2.0.0\n=====\n* Removed NoAccessLogSanic subclass in favour of setup argument\n\n1.3.0\n=====\n* Added Request ID to ``request`` dict\n* fixed move to travis.com\n\n1.2.0\n=====\n* Fixed UA header bug, fixed tests\n\n1.1.1\n=====\n* Pretty much first decent version\n',
    'author': 'Terry Cain',
    'author_email': 'terry@terrys-home.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/terrycain/sanic-json-logging',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
