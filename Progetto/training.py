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
import onesignal
import glob

# Acquisizione di immagini e labels
def face_model():

    # Path for face image database
    path = 'Dataset/'

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("CascadeClassifier/haarcascade_frontalface_default.xml")

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []
    print(*imagePaths)

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        print(id)
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
        #converte l'audio in un vettore di floating point
        #data è il vero e proprio vettore di tipo float32
        #sr è un numero >0 che indica il tasso di campionamento
        data = svt.rms_silence_filter(data)
        mfcc = svt.extract_mfcc(data, sr, winlen=0.025, winstep=0.01)
        mfcc = preprocessing.scale(mfcc)
        #Standardizza un dataset su qualunque asse
        #Standardizzazione di datasets è un requisito comune per molti stimatori in ambito machine-learning
        #implementati in scikit-learn; potrebbero comportarsi in maniera inaspettata se le features individuali
        #non fossero standardizzate normalmente con dati distribuiti
        delta = librosa.feature.delta(mfcc)
        combined = numpy.hstack((mfcc, delta))

        mfcc = combined

        if i == 1:
            results = mfcc
        else:
            results = numpy.vstack((results, mfcc))

    model = sklearn.mixture.GaussianMixture(n_components=audio_number + 1, covariance_type='full', n_init=1)
    #classe che permette di stimare i parametri di una gaussian mixture model
    model.fit(results)
    #stima i parametri del modello con l'algoritmo EM
    #expectation maximization: Lo scopo dell’algoritmo EM è quello di aumentare, e possibilmente di massimizzare,
    #la likelihood dei parametri di un modello probabilistico M rispetto ad un insieme di dati s,
    #risultati di un processo stocastico che coinvolge un processo non noto

    filename = './Trainer/model' + nomefile + ".gmm"
    pickle.dump(model, open(filename, 'wb'))

def remove_photo_user():
    path = 'Dataset'
    photos = glob.glob(path + '/*')
    for f in photos:
        os.remove(f)
    if len(os.listdir(path)) == 0:
        print("Rimozione effettuata con successo\n")
    else:
        print("Impossibile eliminare tutti i file\n")

def remove_wav_files(nomefile, audio_number):
    for i in range (1,audio_number+1):
        if os.path.exists('./Registrazioni/' + nomefile + str(i) + '.wav'):
            os.remove('./Registrazioni/' + nomefile + str(i) + '.wav')
    print("rimozione file wav avvenuta")


def send_notification():
    onesignal_client = onesignal.Client(app_auth_key="N2E4NTNkNzAtYjhjYi00ZTI0LWIzZWUtYTM1YmIyMmQxNzE4",
                                        app_id="1784a5bd-7107-4bda-b628-a19c2034159e")
    new_notification = onesignal.Notification(post_body={"contents": {"en": "Modello creato"}})
    new_notification.post_body["included_segments"] = ["Active Users"]
    new_notification.post_body["buttons"] = [{"id": "id1", "text": "Apri la porta", "icon": "ic_menu_share"},
                                             {"id": "id2", "text": "La porta resta chiusa", "icon": "ic_menu_share"}]

    onesignal_response = onesignal_client.send_notification(new_notification)

    print(onesignal_response.status_code)
    print(onesignal_response.json())



#face_model()
#voice_model('mamma',2)
#voice_model('papa',2)
#voice_model('colucci',2)
#voice_model('pepe',2)
#remove_wav_files('mamma',2)
#remove_photo_user()
#send_notification()
