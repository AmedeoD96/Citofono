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
from string import digits


def voice_model():
    results = numpy.asmatrix(())
    """
    for i in range(1, audio_number + 1):
        AUDIO_FILE = './Registrazioni/' + nomefile + str(i) + '.wav'

        data, sr = librosa.load(AUDIO_FILE, sr=16000, mono=True)
        # converte l'audio in un vettore di floating point
        # data è il vero e proprio vettore di tipo float32
        # sr è un numero >0 che indica il tasso di campionamento
        data = svt.rms_silence_filter(data)
        """
    basepath = "./Registrazioni/"
    i = 0
    for entry in os.listdir(basepath):
        i += 1
        if os.path.isfile(os.path.join(basepath, entry)):
            if entry.endswith(".wav"):
                if i == 1:
                    file_name = str(entry[:-5])
                AUDIO_FILE = basepath + "/" + entry
                data, sr = librosa.load(AUDIO_FILE, sr=16000, mono=True)
                # converte l'audio in un vettore di floating point
                # data è il vero e proprio vettore di tipo float32
                # sr è un numero >0 che indica la frequenza di campionamento
                data = svt.rms_silence_filter(data)
                nyq = 0.5*sr
                cutoff = 250
                normal_cutoff = cutoff / nyq
                b, a = sg.butter(1, normal_cutoff, 'low')
                data = sg.filtfilt(b, a, data)

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

    model = sklearn.mixture.GaussianMixture(n_components=i, covariance_type='full', n_init=1)
    # classe che permette di stimare i parametri di una gaussian mixture model
    model.fit(results)
    # stima i parametri del modello con l'algoritmo EM
    # expectation maximization: Lo scopo dell’algoritmo EM è quello di aumentare, e possibilmente di massimizzare,
    # la likelihood dei parametri di un modello probabilistico M rispetto ad un insieme di dati s,
    # risultati di un processo stocastico che coinvolge un processo non noto

    filename = './Trainer/model' + file_name + ".gmm"
    pickle.dump(model, open(filename, 'wb'))
    remove_wav_files()


def remove_wav_files():
    path = 'Registrazioni'
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)
    if len(os.listdir(path)) == 0:
        print("Rimozione effettuata con successo\n")
    else:
        print("Impossibile eliminare tutti i file\n")