# Speech Enhancement Model Evaluation

This is a python package to evaluate your speech enhancement model performance.

## Installation
`pip install model-evaluation-777 -i https://pypi.org/simple`

## PESQ and STOI Evaluation
```python
def evaluate(ref_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/clean/", deg_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/noisy/", fs=16000):
    '''
    Args:
        ref_dir: reference signal directory
        deg_dir: degration signal directory
    Returns:
        pesq_score_average, stoi_score_average
    '''
```
```python
from model_evaluation import stoi_pesq
pesq_score, stoi_score = stoi_pesq.evaluate(ref_dir=ref_dir, deg_dir=deg_dir, fs=16000)
```