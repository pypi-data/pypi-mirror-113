# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onnion_runtime']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'onnion-rt',
    'version': '0.1.0',
    'description': 'run onnx with only numpy',
    'long_description': '# onnion-rt\n\nNote: This software includes [the work](https://github.com/onnx/onnx) that is distributed in the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).\n\n## Installation\n\n```\n$ pip3 install onnion-rt\n```\n\n## Usage\nSee [tutorial](https://github.com/Idein/onnion/tree/master#tutorial).\n\n## Development Guide\n\n```\n$ poetry install\n```\n\n### How to support new operators\n\n1. Add `onnion_runtime/xxx.py`\n2. Add `from .xxx import Xxx # noqa: F401` to `onnion_runtime/__init__.py`\n3. Update "Supported Operators" in `README.md`\n4. Add `tests/test_xxx.py`\n5. Run tests `poetry run pytest -v`\n6. Format and lint `poetry run pysen run format && poetry run pysen run lint`\n\n## Supported Operators\nThis runtime supports only below operators.\n\n- Add\n  - must be from opsetversion >= 7\n- Concat\n- Div\n  - must be from opsetversion >= 7\n- Exp\n- Mul\n  - must be from opsetversion >= 7\n- Slice\n- Sub\n  - must be from opsetversion >= 7\n',
    'author': 'Idein Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Idein/onnion/tree/master/runtime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
