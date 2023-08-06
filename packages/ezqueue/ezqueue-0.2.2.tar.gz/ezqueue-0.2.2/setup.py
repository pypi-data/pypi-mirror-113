# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ezqueue']
setup_kwargs = {
    'name': 'ezqueue',
    'version': '0.2.2',
    'description': 'Easy queue allows for fixed size array and unique keys',
    'long_description': '# ezqueue \nZero dependency in-memory queue\n\n[![Python](https://img.shields.io/badge/python-3.7-blue)]()\n[![codecov](https://codecov.io/gh/jwcnewton/ezqueue/branch/main/graph/badge.svg)](https://codecov.io/gh/jwcnewton/ezqueue)\n[![Documentation Status](https://readthedocs.org/projects/ezqueue/badge/?version=latest)](https://ezqueue.readthedocs.io/en/latest/?badge=latest)\n[![Build](https://github.com/jwcnewton/ezqueue/workflows/build/badge.svg)](https://github.com/jwcnewton/ezqueue/actions/workflows/build.yml)\n[![Deploy](https://github.com/jwcnewton/ezqueue/actions/workflows/deploy.yml/badge.svg)](https://github.com/jwcnewton/ezqueue/actions/workflows/deploy.yml)\n\n\n## Installation\n\n```bash\n$ pip install -i https://test.pypi.org/simple/ ezqueue\n```\n\n## Features\n\n- TODO\n\n## Dependencies\n\n- TODO\n\n## Usage\n\n- TODO\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://ezqueue.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/jwcnewton/ezqueue/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'jwcnewton',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jwcnewton/ezqueue',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
