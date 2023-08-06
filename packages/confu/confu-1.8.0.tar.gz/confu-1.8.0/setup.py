# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['confu', 'confu.schema']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'confu',
    'version': '1.8.0',
    'description': 'Configuration file validation and generation',
    'long_description': '# Confu\n\n[![PyPI](https://img.shields.io/pypi/v/confu.svg?maxAge=60)](https://pypi.python.org/pypi/confu)\n[![PyPI](https://img.shields.io/pypi/pyversions/confu.svg?maxAge=600)](https://pypi.python.org/pypi/confu)\n[![Tests](https://github.com/20c/confu/workflows/tests/badge.svg)](https://github.com/20c/confu)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/confu/master.svg?maxAge=60)](https://codecov.io/github/20c/confu)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/20c/confu.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/20c/confu/context:python)\n\nConfiguration validation and generation\n\n\n## Note PyPI package renamed\n\nAll current releases will use the name `confu`. Please change any package requirements and imports from `cfu` to `confu`\n\n## Documentation\n\n  - **stable**: https://confu.readthedocs.io/en/stable/quickstart/\n  - **latest**: https://confu.readthedocs.io/en/latest/quickstart/\n\n## License\n\nCopyright 2016-2021 20C, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this software except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/confu',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
