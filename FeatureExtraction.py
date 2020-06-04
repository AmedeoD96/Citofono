from os import path
import speaker_verification_toolkit.tools as svt
import python_speech_features as psf
from sklearn import preprocessing
import numpy
import librosa
import noisereduce as nr
import scipy


def obtainMFCCfromWav (index, nomefile):

    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "./wavFiles/"+nomefile+str(index)+".wav")

    data, sr = librosa.load(AUDIO_FILE, sr=16000, mono=True)
    data = svt.rms_silence_filter(data)
    #chroma = librosa.feature.chroma_cqt(y=data, sr=sr)
    #chroma_med = librosa.decompose.nn_filter(chroma, aggregate = numpy.median,metric = 'cosine')
    #data = librosa.decompose.nn_filter(data)
    mfcc = svt.extract_mfcc(data, sr, winlen=0.025, winstep=0.01)
    mfcc = preprocessing.scale(mfcc) #standardizza il dataset lungo un asse
    delta = librosa.feature.delta(mfcc)
    combined = numpy.hstack((mfcc, delta))
    numpy.savetxt("./mfcc/mfcc"+nomefile+str(index)+".txt",combined)
    return combined

obtainMFCCfromWav(1,"lillo")








