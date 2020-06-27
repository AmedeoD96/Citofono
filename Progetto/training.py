import os
import speaker_verification_toolkit.tools as svt
from sklearn import preprocessing
import librosa
import sklearn.mixture
import numpy
import pickle
import glob
import scipy.signal as sg
import warnings
warnings.filterwarnings("ignore")


def voice_model():
    results = numpy.asmatrix(())
    basepath = "./Registrazioni/"
    i = 0
    for entry in os.listdir(basepath):
        i += 1
        if os.path.isfile(os.path.join(basepath, entry)):
            if entry.endswith(".wav"):
                if i == 1:
                    file_name = str(entry[:-5])
                audio_file = basepath + "/" + entry
                # converte l'audio in un vettore di floating point
                # data è il vero e proprio vettore di tipo float32
                # sr è un numero >0 che indica la frequenza di campionamento
                data, sr = librosa.load(audio_file, sr=16000, mono=True)

                nyq = 0.5 * sr
                cutoff = 250
                normal_cutoff = cutoff / nyq

                numerator, denominator = sg.butter(1, normal_cutoff, 'low')
                data = sg.filtfilt(numerator, denominator, data)
                data = svt.rms_silence_filter(data)

                mfcc = svt.extract_mfcc(data, sr, winlen=0.025, winstep=0.01)

                # Standardizza un dataset secondo la standard-scaler
                mfcc = preprocessing.scale(mfcc)

                delta = librosa.feature.delta(mfcc)
                combined = numpy.hstack((mfcc, delta))

                mfcc = combined

                if i == 1:
                    results = mfcc
                else:
                    results = numpy.vstack((results, mfcc))

    # classe che permette di stimare i parametri di una gaussian mixture model
    model = sklearn.mixture.GaussianMixture(n_components=i, covariance_type='full', n_init=1)

    # stima i parametri del modello con l'algoritmo EM
    model.fit(results)

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
