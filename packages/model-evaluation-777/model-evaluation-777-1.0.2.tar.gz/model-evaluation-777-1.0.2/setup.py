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
    'version': '1.0.2',
    'description': 'Evaluate speech enhancemnt model performance',
    'long_description': '# Speech Enhancement Model Evaluation\n\nThis is a python package to evaluate your speech enhancement model performance.\n\n## Installation\n`pip install model-evaluation-777 -i https://pypi.org/simple`\n\n## PESQ and STOI Evaluation\n```python\ndef evaluate(ref_dir="/media/youwei/Chauncey\'s/VERSO_Dataset/test/clean/", deg_dir="/media/youwei/Chauncey\'s/VERSO_Dataset/test/noisy/", fs=16000):\n    \'\'\'\n    Args:\n        ref_dir: reference signal directory\n        deg_dir: degration signal directory\n        fs: sample rate\n    Returns:\n        pesq_score_average, stoi_score_average\n    \'\'\'\n```\n```python\nfrom model_evaluation import stoi_pesq\n\npesq_score, stoi_score = stoi_pesq.evaluate(ref_dir=ref_dir, deg_dir=deg_dir, fs=16000)\n```\n\n## Plot SNR vs PESQ\n```python\ndef plot_snr_pesq(out_dir, enh_dir, ref_dir="/media/youwei/Chauncey\'s/VERSO_Dataset/test/clean/", deg_dir="/media/youwei/Chauncey\'s/VERSO_Dataset/test/noisy/", fs=16000):\n    \'\'\'\n    Args:\n        out_dir: directory to save figure\n        enh_dir: enhanced signal directory\n        ref_dir: reference signal directory\n        deg_dir: degration signal directory\n        fs: sample rate\n    Returns:\n        snr vs pesq score data\n    \'\'\'\n```\nThe SNR vs PESQ figure will save to out_dir automatically.\n```python\nfrom model_evaluation import stoi_pesq\n\ndata = stoi_pesq.plot_snr_pesq(out_dir=out_dir, enh_dir=enh_dir)\n```\n\n## Plot SNR vs STOI\n```python\ndef plot_snr_stoi(out_dir, enh_dir, ref_dir="/media/youwei/Chauncey\'s/VERSO_Dataset/test/clean/", deg_dir="/media/youwei/Chauncey\'s/VERSO_Dataset/test/noisy/", fs=16000):\n    \'\'\'\n    Args:\n        out_dir: directory to save figure\n        enh_dir: enhanced signal directory\n        ref_dir: reference signal directory\n        deg_dir: degration signal directory\n        fs: sample rate\n    Returns:\n        snr vs stoi score data\n    \'\'\'\n```\nThe SNR vs STOI figure will save to out_dir automatically.\n```python\nfrom model_evaluation import stoi_pesq\n\ndata = stoi_pesq.plot_snr_stoi(out_dir=out_dir, enh_dir=enh_dir)\n```',
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
