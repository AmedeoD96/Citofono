import cv2
import numpy as np
from PIL import Image
import os
import speaker_verification_toolkit.tools as svt
from sklearn import preprocessing
import librosa
import sklearn.mixture
import numpy
import pickle

# Acquisizione di immagini e labels
def face_model():

    # Path for face image database
    path = 'Dataset/'

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("CascadeClassifier/haarcascade_frontalface_default.xml")

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)


    print("\n Fase di addestramento. Attendere...")
    recognizer.train(faceSamples, np.array(ids))



    # Salvo il modello
    recognizer.write('./Trainer/trainer.yml')

    # Stampo il numero di facce imparate
    print("\n [INFO] {0} Facce unoarate. Uscita in corso...".format(len(np.unique(ids))))

def voice_model (nomefile, audio_number):
    results = numpy.asmatrix(())

    for i in range(1, audio_number + 1):
        AUDIO_FILE = './Registrazioni/' + nomefile + str(i) + '.wav'

        data, sr = librosa.load(AUDIO_FILE, sr=16000, mono=True)
        data = svt.rms_silence_filter(data)
        mfcc = svt.extract_mfcc(data, sr, winlen=0.025, winstep=0.01)
        mfcc = preprocessing.scale(mfcc)
        delta = librosa.feature.delta(mfcc)
        combined = numpy.hstack((mfcc, delta))

        mfcc = combined

        if i == 1:
            results = mfcc
        else:
            results = numpy.vstack((results, mfcc))

    model = sklearn.mixture.GaussianMixture(n_components=audio_number + 1, covariance_type='full', n_init=1)
    model.fit(results)

    filename = './Trainer/model' + nomefile + ".gmm"
    pickle.dump(model, open(filename, 'wb'))

def remove_photo_user():
    id = 1
    while (True):
        for x in range(1, 31):
            if os.path.exists('./Dataset/User.' + str(id) + '.' + str(x) + '.jpg'):
                os.remove('./Dataset/User.' + str(id) + '.' + str(x) + '.jpg')
        if os.path.exists('./Dataset/User.' + str(id+1) + '.1.jpg'):
            id += 1
        else:
            break
    print("Rimozione effettuata con successo")

def remove_wav_files(nomefile, audio_number):
    for i in range (1,audio_number+1):
        if os.path.exists('./Registrazioni/' + nomefile + str(i) + '.wav'):
            os.remove('./Registrazioni/' + nomefile + str(i) + '.wav')
    print("rimozione file wav avvenuta")



#face_model()
#voice_model('alessandro', 2)
#voice_model('amedeo',2)
#voice_model('colucci',2)
#voice_model('mamma',2)
#voice_model('papa',2)
#voice_model('pepe',2)
#remove_wav_files('mamma',2)
#remove_photo_user()