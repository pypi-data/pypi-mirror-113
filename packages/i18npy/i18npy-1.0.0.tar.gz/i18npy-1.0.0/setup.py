# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['i18npy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'i18npy',
    'version': '1.0.0',
    'description': 'Internationalization library. Python implementation of roddeh/i18njs',
    'long_description': '# i18npy\n\n[![PyPI](https://img.shields.io/pypi/v/i18npy)](https://pypi.org/project/i18npy/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/i18npy)](https://github.com/marverix/i18npy/actions/workflows/tests.yml)\n[![Codecov](https://img.shields.io/codecov/c/gh/marverix/i18npy?token=NPX0JP4458)](https://app.codecov.io/gh/marverix/i18npy)\n[![GitHub](https://img.shields.io/github/license/marverix/i18npy)](https://tldrlegal.com/license/mit-license)\n\nThis is Python implementation of [roddeh/i18njs](https://github.com/roddeh/i18njs) (http://i18njs.com/).\nIt\'s fully compatible with it\'s  JSON dictionaries syntax.\n\n## Usage\n\n### Installation\n\n```sh\npip install i18npy\n```\n\n### Samples\n\n#### With external dictionary and global i18n instance\n\npl.json\n\n```json\n{\n  "values": {\n    "Hello World": "Witaj świecie",\n    "I have %n cookies": [\n      [null, null, "Nie ma rączek, nie ma ciasteczek"],\n      [0, 0, "Nie mam ciasteczek"],\n      [1, 1, "Mam jedno ciasteczko"],\n      [2, 4, "Mam %n ciasteczka"],\n      [5, null, "Mam %n ciasteczek"]\n    ]\n  }\n}\n\n```\n\ncode\n\n```python\nfrom i18npy import i18n, i18n_load\n\ni18n_load("./pl.json")\n\ni18n("Hello World")\n# Witaj świecie\n\nKEY = "I have %n cookies"\ni18n(KEY, None)\n# Nie ma rączek, nie ma ciasteczek\n\ni18n(KEY, 0)\n# Nie mam ciasteczek\n\ni18n(KEY, 1)\n# Mam jedno ciasteczko\n\ni18n(KEY, 3)\n# Mam 3 ciasteczka\n\ni18n(KEY, 5)\n# Mam 5 ciasteczek\n```\n\n#### Create translator instances\n\n```python\nimport i18npy\n\nlang_pl = i18npy.create({\n  "values": {\n    "Hello World": "Witaj świecie",\n    "I have %n cookies": [\n      [None, None, "Nie ma rączek, nie ma ciasteczek"],\n      [0, 0, "Nie mam ciasteczek"],\n      [1, 1, "Mam jedno ciasteczko"],\n      [2, 4, "Mam %n ciasteczka"],\n      [5, None, "Mam %n ciasteczek"]\n    ]\n  }\n})\n\nlang_pl.translate("Hello World")\n# Witaj świecie\n\nlang_pl.translate("I have %n cookies", 3)\n# Mam 3 ciasteczka\n```\n\n## Word of appreciation \n\nThe original i18njs library ha been written by [roddeh](https://github.com/roddeh/).\nThe library code is based on his code, which is also licensed by MIT.\n\n## License\n\nThis project is licensed under MIT License - see the [LICENSE](LICENSE) file for details.\n',
    'author': 'Marek Sierociński',
    'author_email': 'mareksierocinski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marverix/i18npy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
