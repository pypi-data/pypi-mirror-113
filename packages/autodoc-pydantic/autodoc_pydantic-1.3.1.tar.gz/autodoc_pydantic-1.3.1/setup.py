# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.autodoc_pydantic']

package_data = \
{'': ['*'], 'sphinxcontrib.autodoc_pydantic': ['css/*']}

install_requires = \
['Sphinx>=3.4', 'pydantic>=1.5']

extras_require = \
{'dev': ['sphinx-rtd-theme>=0.5,<0.6',
         'sphinx-tabs>=2,<3',
         'sphinx-copybutton>=0.4,<0.5',
         'pytest>=6,<7',
         'coverage>=5,<6',
         'flake8>=3,<4',
         'tox>=3,<4'],
 'docs': ['sphinx-rtd-theme>=0.5,<0.6',
          'sphinx-tabs>=2,<3',
          'sphinx-copybutton>=0.4,<0.5'],
 'test': ['pytest>=6,<7', 'coverage>=5,<6']}

setup_kwargs = {
    'name': 'autodoc-pydantic',
    'version': '1.3.1',
    'description': 'Seamlessly integrate pydantic models in your Sphinx documentation.',
    'long_description': "![Autodoc Pydantic](https://raw.githubusercontent.com/mansenfranzen/autodoc_pydantic/main/docs/source/material/logo_black.svg)\n\n[![PyPI version](https://badge.fury.io/py/autodoc-pydantic.svg)](https://badge.fury.io/py/autodoc-pydantic)\n![Master](https://github.com/mansenfranzen/autodoc_pydantic/actions/workflows/tests.yml/badge.svg)\n![Python](https://img.shields.io/badge/python-3.6+-blue.svg)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/30a083d784f245a98a0d5e6857708cc8)](https://www.codacy.com/gh/mansenfranzen/autodoc_pydantic/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mansenfranzen/autodoc_pydantic&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/30a083d784f245a98a0d5e6857708cc8)](https://www.codacy.com/gh/mansenfranzen/autodoc_pydantic/dashboard?utm_source=github.com&utm_medium=referral&utm_content=mansenfranzen/autodoc_pydantic&utm_campaign=Badge_Coverage)\n[![Documentation Status](https://readthedocs.org/projects/autodoc-pydantic/badge/?version=latest)](https://autodoc-pydantic.readthedocs.io/en/latest/?badge=latest)\n\nYou love [pydantic](https://pydantic-docs.helpmanual.io/) ❤ and you want to\ndocument your models and configuration settings with [sphinx](https://www.sphinx-doc.org/en/master/)?\n\nPerfect, let's go. But wait, sphinx' [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)\ndoes not integrate too well with pydantic models 😕.\n\nDon't worry - just `pip install autodoc_pydantic` ☺.\n\n## Features\n\n- 💬 provides default values, alias and constraints for model fields\n- 🔗 adds hyperlinks between validators and corresponding fields\n- 📃 includes collapsable model json schema\n- 🏄 natively integrates with autodoc and autosummary extensions\n- 📎 defines explicit pydantic prefixes for models, settings, fields, validators and model config\n- 📋 shows summary section for model configuration, fields and validators\n- 👀 hides overloaded and redundant model class signature\n- 📚 sorts fields, validators and model config within models by type\n- 🍀 Supports `pydantic >= 1.5.0` and `sphinx >= 3.4.0`\n\n### Comparison between autodoc sphinx and autodoc pydantic\n\n[![Comparison](https://raw.githubusercontent.com/mansenfranzen/autodoc_pydantic/main/docs/source/material/example_comparison_v1.0.0.gif)](https://autodoc-pydantic.readthedocs.io/en/latest/examples.html#default-configuration)\n\nTo see those features in action, jump over to the [example documentation](https://autodoc-pydantic.readthedocs.io/en/latest/examples.html#default-configuration) to compare\nthe appearance of standard sphinx autodoc with *autodoc_pydantic*.\n\n## Documentation\n\nFor more details, please visit the official [documentation](https://autodoc-pydantic.readthedocs.io/en/latest/):\n\n- [Installation](https://autodoc-pydantic.readthedocs.io/en/latest/installation.html)\n- [Configuration](https://autodoc-pydantic.readthedocs.io/en/latest/configuration.html)\n- [Usage](https://autodoc-pydantic.readthedocs.io/en/latest/usage.html)\n- [Examples](https://autodoc-pydantic.readthedocs.io/en/latest/examples.html)\n\n## Acknowledgements\n\nThanks to great open source projects [sphinx](https://www.sphinx-doc.org/en/master/),\n[pydantic](https://pydantic-docs.helpmanual.io/) and\n[poetry](https://python-poetry.org/) (and so many more) ❤!\n",
    'author': 'mansenfranzen',
    'author_email': 'franz.woellert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mansenfranzen/autodoc_pydantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
