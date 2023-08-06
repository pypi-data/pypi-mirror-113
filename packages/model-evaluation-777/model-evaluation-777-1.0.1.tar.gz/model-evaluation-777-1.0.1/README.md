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
        fs: sample rate
    Returns:
        pesq_score_average, stoi_score_average
    '''
```
```python
from model_evaluation import stoi_pesq

pesq_score, stoi_score = stoi_pesq.evaluate(ref_dir=ref_dir, deg_dir=deg_dir, fs=16000)
```

## Plot SNR vs PESQ
```python
def plot_snr_pesq(out_dir, enh_dir, ref_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/clean/", deg_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/noisy/", fs=16000):
    '''
    Args:
        out_dir: directory to save figure
        enh_dir: enhanced signal directory
        ref_dir: reference signal directory
        deg_dir: degration signal directory
        fs: sample rate
    Returns:
        snr vs pesq score data
    '''
```
The SNR vs PESQ figure will save to out_dir automatically.
```python
from model_evaluation import stoi_pesq

data = stoi_pesq.plot_snr_pesq(out_dir=out_dir, enh_dir=enh_dir)
```

## Plot SNR vs STOI
```python
def plot_snr_stoi(out_dir, enh_dir, ref_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/clean/", deg_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/noisy/", fs=16000):
    '''
    Args:
        out_dir: directory to save figure
        enh_dir: enhanced signal directory
        ref_dir: reference signal directory
        deg_dir: degration signal directory
        fs: sample rate
    Returns:
        snr vs stoi score data
    '''
```
The SNR vs STOI figure will save to out_dir automatically.
```python
from model_evaluation import stoi_pesq

data = stoi_pesq.plot_snr_stoi(out_dir=out_dir, enh_dir=enh_dir)
```