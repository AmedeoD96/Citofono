import cv2
import numpy as np
import os
import speaker_verification_toolkit.tools as svt
from sklearn import preprocessing
import librosa
import sklearn.mixture
import numpy
import pickle
import onesignal
import glob
import scipy.signal as sg
import wave


def voice_model(nomefile, audio_number):
    results = numpy.asmatrix(())

    for i in range(1, audio_number + 1):
        AUDIO_FILE = './Registrazioni/' + nomefile + str(i) + '.wav'

        data, sr = librosa.load(AUDIO_FILE, sr=16000, mono=True)
        # converte l'audio in un vettore di floating point
        # data è il vero e proprio vettore di tipo float32
        # sr è un numero >0 che indica il tasso di campionamento
        data = svt.rms_silence_filter(data)

        #fr = 44100*16*2
        #b, a = sg.butter(4, 500. / (fr / 2.), 'low')
        #data = sg.filtfilt(b, a, data)
        fs = 44100.0
        lowcut = 500.0
        highcut = 1250.0
        data = butter_bandpass_filter(data, lowcut, highcut, fs, order=6)

        mfcc = svt.extract_mfcc(data, sr, winlen=0.025, winstep=0.01)
        mfcc = preprocessing.scale(mfcc)
        # Standardizza un dataset su qualunque asse
        # Standardizzazione di datasets è un requisito comune per molti stimatori in ambito machine-learning
        # implementati in scikit-learn; potrebbero comportarsi in maniera inaspettata se le features individuali
        # non fossero standardizzate normalmente con dati distribuiti
        delta = librosa.feature.delta(mfcc)
        combined = numpy.hstack((mfcc, delta))

        mfcc = combined

        if i == 1:
            results = mfcc
        else:
            results = numpy.vstack((results, mfcc))

    model = sklearn.mixture.GaussianMixture(n_components=audio_number + 1, covariance_type='full', n_init=1)
    # classe che permette di stimare i parametri di una gaussian mixture model
    model.fit(results)
    # stima i parametri del modello con l'algoritmo EM
    # expectation maximization: Lo scopo dell’algoritmo EM è quello di aumentare, e possibilmente di massimizzare,
    # la likelihood dei parametri di un modello probabilistico M rispetto ad un insieme di dati s,
    # risultati di un processo stocastico che coinvolge un processo non noto

    filename = './Trainer/model' + nomefile + ".gmm"
    pickle.dump(model, open(filename, 'wb'))


def remove_wav_files(nomefile, audio_number):
    for i in range(1, audio_number + 1):
        if os.path.exists('./Registrazioni/' + nomefile + str(i) + '.wav'):
            os.remove('./Registrazioni/' + nomefile + str(i) + '.wav')
    print("rimozione file wav avvenuta")

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sg.butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sg.lfilter(b, a, data)
    return y


#voice_model('input',3)
#remove_wav_files('input', 3)

voice_model('alessandro',3)
voice_model('amedeo',2)
voice_model('colucci',2)
voice_model('lenoci',3)
voice_model('mamma',2)
voice_model('papa',2)
voice_model('pepe',2)
