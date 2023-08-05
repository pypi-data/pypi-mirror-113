import os
import librosa
from pesq import pesq
from pystoi import stoi

def evaluate(ref_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/clean/", deg_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/noisy/", fs=16000):
    '''
    Args:
        ref_dir: reference signal directory
        deg_dir: degration signal directory
    Returns:
        pesq_score_average, stoi_score_average
    '''
    ref_signals = os.listdir(ref_dir)
    ref_signals.sort()
    deg_signals = os.listdir(deg_dir)
    deg_signals.sort()
    pesq_sum, stoi_sum = 0, 0
    for i in range(len(ref_signals)):
        ref, _ = librosa.load(os.path.join(ref_dir, ref_signals[i]), sr=fs)
        deg, _ = librosa.load(os.path.join(deg_dir, deg_signals[i]), sr=fs)
        length = min(len(ref), len(deg))
        pesq_score = pesq(fs, ref[:length], deg[:length], 'wb')
        stoi_score = stoi(ref[:length], deg[:length], fs, extended=False)
        pesq_sum += pesq_score
        stoi_sum += stoi_score
    return pesq_sum / len(ref_signals), stoi_sum / len(ref_signals)

def plot_snr_stoi():
    pass

def plot_pesq_stoi():
    pass

# print(evaluate())