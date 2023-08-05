# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['model_evaluation']

package_data = \
{'': ['*']}

install_requires = \
['librosa>=0.8.1,<0.9.0',
 'numpy>=1.21.0,<2.0.0',
 'pesq>=0.0.3,<0.0.4',
 'pystoi>=0.3.3,<0.4.0']

setup_kwargs = {
    'name': 'model-evaluation-777',
    'version': '0.0.3',
    'description': 'Evaluate speech enhancemnt model performance',
    'long_description': None,
    'author': 'Chengwei Ouyang',
    'author_email': 'chengwei@evocolabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
