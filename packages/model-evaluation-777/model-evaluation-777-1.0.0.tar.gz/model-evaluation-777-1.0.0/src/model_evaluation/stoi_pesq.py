import os
import librosa
from pesq import pesq
from pystoi import stoi
from matplotlib import pyplot as plt 

def evaluate(ref_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/clean/", deg_dir="/media/youwei/Chauncey's/VERSO_Dataset/test/noisy/", fs=16000):
    '''
    Args:
        ref_dir: reference signal directory
        deg_dir: degration signal directory,
        fs: sample rate
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
    pesq_scores = []
    noisy_scores = [1.1284073889255524, 1.1682419955730439, 1.2397681593894958, 1.1706185042858124, 1.2197929322719574, 1.3456271052360536, 1.2534406006336212, 1.31161567568779, 1.313832587003708, 1.4032578110694884, 1.4999170362949372, 1.446747177839279, 1.5079774379730224, 1.517793893814087, 1.8037997424602508, 1.7001607239246368, 1.659944123029709, 2.072042614221573, 1.8786624729633332, 2.028641825914383, 2.377078503370285, 2.323824572563171, 2.3018155217170717, 2.606920635700226, 2.572139173746109]
    for i in range(25):
        sum = 0
        for j in range(20):
            ref, _ = librosa.load(os.path.join(ref_dir, '{}.wav'.format(str(i*20+j))), sr=fs)
            deg, _ = librosa.load(os.path.join(enh_dir, '{}.wav'.format(str(i*20+j))), sr=fs)
            length = min(len(ref), len(deg))
            pesq_score = pesq(fs, ref[:length], deg[:length], 'wb')
            sum += pesq_score
        pesq_scores.append(sum / 20)
    snr = [i - 5 for i in range(25)]
    plt.title("SNR vs PESQ") 
    plt.xlabel("SNR") 
    plt.ylabel("PESQ") 
    plt.plot(snr, noisy_scores, label='noisy')
    plt.plot(snr, pesq_scores, label='enhanced')
    plt.grid(True)
    plt.legend()
    plt.savefig(fname=os.path.join(out_dir, "pesq.png"))
    return [{'snr': str(snr[i]) + 'dB', 'noisy_score': noisy_scores[i], 'enhanced_score': pesq_scores[i]} for i in range(25)]

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
    stoi_scores = []
    noisy_scores = [0.5447706106062677, 0.6472889786894999, 0.6764422443156219, 0.6486002775356061, 0.6315979957854213, 0.6725807605535581, 0.7298389319439933, 0.6595894740615565, 0.6902966119447709, 0.7293898720841745, 0.7044035756873229, 0.7442884243904075, 0.7096693150036287, 0.7939196044754203, 0.8226736958153044, 0.8269072662330524, 0.8390934447762632, 0.8154656631674244, 0.8165304624244314, 0.8524859721966346, 0.8401341330114155, 0.8548401850733051, 0.878069022974777, 0.8745229879096723, 0.8965910438312873]
    for i in range(25):
        sum = 0
        for j in range(20):
            ref, _ = librosa.load(os.path.join(ref_dir, '{}.wav'.format(str(i*20+j))), sr=fs)
            deg, _ = librosa.load(os.path.join(enh_dir, '{}.wav'.format(str(i*20+j))), sr=fs)
            length = min(len(ref), len(deg))
            stoi_score = stoi(ref[:length], deg[:length], fs, extended=False)
            sum += stoi_score
        stoi_scores.append(sum / 20)
    snr = [i - 5 for i in range(25)]
    plt.title("SNR vs STOI") 
    plt.xlabel("SNR") 
    plt.ylabel("STOI") 
    plt.plot(snr, noisy_scores, label='noisy')
    plt.plot(snr, stoi_scores, label='enhanced')
    plt.grid(True)
    plt.legend()
    plt.savefig(fname=os.path.join(out_dir, "stoi.png"))
    return [{'snr': str(snr[i]) + 'dB', 'noisy_score': noisy_scores[i], 'enhanced_score': stoi_scores[i]} for i in range(25)]