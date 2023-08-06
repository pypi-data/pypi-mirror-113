# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['carrot_rcc']
entry_points = \
{'console_scripts': ['carrot-rcc = carrot_rcc:main']}

setup_kwargs = {
    'name': 'carrot-rcc',
    'version': '0.2.0',
    'description': 'Camunda external task Robot Framework RCC client',
    'long_description': '```bash\nusage: carrot-rcc [<robots>...]\n                  [--base-url] [--authorization]\n                  [--worker-id] [--max-tasks] [--poll-interval] [--log-level]\n                  [--rcc-executable] [--rcc-encoding] [--rcc-telemetry]\n                  [-h] [--help]\n\n<robots> could also be passed as a comma separated env RCC_ROBOTS\n\noptions:\n\n  --base-url[=<url>]                       [env: CAMUNDA_API_BASE_URL] [default: http://localhost:8080/engine-rest]\n  --authorization[=<header>]               [env: CAMUNDA_API_AUTHORIZATION] [example: Basic ZGVtbzpkZW1v]\n\n  --worker-id[=<string>]                   [env: CLIENT_WORKER_ID] [default: carrot-rcc]\n  --max-tasks[=<cpus>]                     [env: CLIENT_MAX_TASKS] [default: [cpu count]]\n  --poll-interval[=<milliseconds>]         [env: CLIENT_POLL_INTERVAL] [default: 30000]\n  --log-level[=<debug|info|warn|error>]    [env: CLIENT_LOG_LEVEL] [default: info]\n\n  --rcc-executable[=<path>]                [env: RCC_EXECUTABLE] [default: rcc]\n  --rcc-encoding[=<encoding>]              [env: RCC_ENCODING] [default: utf-8]\n  --rcc-telemetry                          [env: RCC_TELEMETRY] (default: do not track)\n\n  -h, --help\n```\n',
    'author': 'Asko Soukka',
    'author_email': 'asko.soukka@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datakurre/carrot-rcc',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
