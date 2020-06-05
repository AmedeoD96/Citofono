import cv2
import numpy as np
import os
import sounddevice as sd
from scipy.io.wavfile import write
import pickle
from sklearn import preprocessing
import librosa
import speaker_verification_toolkit.tools as svt


# Variabili riconoscimento del volto
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Trainer/trainer.yml')
cascadePath = "CascadeClassifier/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
id = 0

# Nome associato all'ID
# TODO: DA MODIFICARE. NON DEVE ESSERE UNA LISTA STATICA
names = ['Sconosciuto', 'Amedeo', 'Enzo', 'Alessandro']




# Variabili riconoscimento voce
models  = []
speakers  = []

def readAllGMMs():
    fs = 44100
    seconds = 5
    print("Avvio riconoscimento vocale: parla\n")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('Registrazioni/input' + str(1000) + '.wav', fs, myrecording)

    data, sr = librosa.load('Registrazioni/input' + str(1000) + '.wav', sr=16000, mono=True)
    data = svt.rms_silence_filter(data)

    mfcc = svt.extract_mfcc(data, sr, winlen=0.025, winstep=0.01)
    mfcc = preprocessing.scale(mfcc)  # standardizza il dataset lungo un asse
    delta = librosa.feature.delta(mfcc)
    combined = np.hstack((mfcc, delta))

    basepath = "./Trainer"
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            if entry.endswith(".gmm"):
                #modelpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./models/" + entry)
                gmmReaded = pickle.load(open(basepath + "/" +entry, 'rb'))
                speakers.append(entry)
                models.append(gmmReaded)

    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(combined))
        log_likelihood[i] = scores.sum()
        # Compute the per-sample average log-likelihood of the given data

    winner = np.argmax(log_likelihood)
    print(" trovato - ", speakers[winner])
    confidenza_audio = (((log_likelihood[winner]-55)*100)/6)
    if(confidenza_audio > 100):
        print("con il valore di 100%")
    else:
        print("con il valore di", confidenza_audio)
    print("tutti i valori sono:")
    print(((log_likelihood-55)*100)/6)

readAllGMMs()


# Attivo la camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)  #Larghezza
cam.set(4, 480)  #Altezza

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=8,
        minSize=(int(minW), int(minH))
    )
    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        # Se la confidenza è meno di 100 allora è perfetta
        if(confidence < 100):
            id = names[id]
            confidence = "{0}%".format(round(100-confidence))
        else:
            id = "Sconosciuto"
            confidence = "{0}%".format(round(100 - confidence))

        cv2.putText(
            img,
            str(id),
            (x+5, y-5),
            font,
            1,
            (255, 255, 255),
            2
        )
        cv2.putText(
            img,
            str(confidence),
            (x+5, y+h+5),
            font,
            1,
            (255, 255, 0),
            1
        )
    cv2.imshow('camera', img)
    k = cv2.waitKey(10) & 0xff  # Premi ESC per uscire
    if k == 27:
        break

print("\n Uscita in corso...")
cam.release()
cv2.destroyAllWindows()



