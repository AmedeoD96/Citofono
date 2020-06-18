import cv2
import numpy as np
import os
import sounddevice as sd
from scipy.io.wavfile import write
import pickle
from sklearn import preprocessing
import librosa
import speaker_verification_toolkit.tools as svt
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import scale
from sklearn.preprocessing import maxabs_scale
from sklearn.preprocessing import robust_scale
import time
from face_trainer import *
import onesignal
import training
import scipy.signal as sg

# Variabili riconoscimento voce
models = []
speakers = []


def read_all_gmms():
    find = False
    fs = 44100
    seconds = 5
    print("Avvio riconoscimento vocale: parla\n")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('Registrazioni/input' + str(1000) + '.wav', fs, myrecording)

    data, sr = librosa.load('Registrazioni/input' + str(1000) + '.wav', sr=16000, mono=True)
    data = svt.rms_silence_filter(data)

    fs = 44100.0
    nyq = 0.5 * fs
    cutoff = 250
    normal_cutoff = cutoff / nyq
    b, a = sg.butter(1, normal_cutoff, 'low')
    data = sg.filtfilt(b, a, data)

    mfcc = svt.extract_mfcc(data, sr, winlen=0.025, winstep=0.01)
    mfcc = preprocessing.scale(mfcc)  # standardizza il dataset lungo un asse
    delta = librosa.feature.delta(mfcc)
    combined = np.hstack((mfcc, delta))

    basepath = "./Trainer"
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            if entry.endswith(".gmm"):
                # modelpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./models/" + entry)
                gmm_readed = pickle.load(open(basepath + "/" + entry, 'rb'))
                speakers.append(entry)
                models.append(gmm_readed)

    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(combined))
        # Calcola la probabilità log pesata per campione del parametro.
        # ritorna Log likelihood del Gaussian mixture dato il parametro combined.
        log_likelihood[i] = scores.sum()
        # Compute the media per campione in scala log-likelihood del dato ottenuto

    print(f"Log likelihood: {log_likelihood}")
    winner = np.argmax(log_likelihood)
    print(" trovato - ", speakers[winner])
    # scaler = MinMaxScaler()
    # scaler.fit(np.asmatrix(log_likelihood))
    # print(scaler.transform(np.asmatrix(log_likelihood)))
    print("minmax")
    print(minmax_scale(log_likelihood))
    print("scale")
    trovato = scale(log_likelihood)
    if trovato[winner] >= 1:
        print("Trovato\n")
        print(scale(log_likelihood))
        print(speakers[winner])
        find = True
    else:
        print("Non trovato\n")


    confidenza_audio = (((log_likelihood[winner] - 55) * 100) / 6)
    if (confidenza_audio > 100):
        print("con il valore di 100%")
    else:
        print("con il valore di", confidenza_audio)
    print("tutti i valori sono:")
    print(((log_likelihood - 55) * 100) / 6)
    if os.path.exists("./Registrazioni/input1000.wav"):
        os.remove("./Registrazioni/input1000.wav")
    return find


def face_recognize():
    find = read_all_gmms()
    print("Inquadra il tuo volto\n")
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    cascade = cv2.CascadeClassifier('./CascadeClassifier/haarcascade_frontalface_default.xml')

    # Carico il database
    db_path = "./Dataset/embeddings.pickle"
    database = pickle.load(open(db_path, "rb"))

    time.sleep(1.0)

    start_time = time.time()

    while True:
        curr_time = time.time()

        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face = cascade.detectMultiScale(gray, 1.05, 8)
        name = "Sconosciuto"

        if len(face) == 1:
            for (x, y, w, h) in face:
                roi = frame[y - 10:y + h + 10, x - 10:x + w + 10]

                fh, fw = roi.shape[:2]
                min_dist = 100

                # Verifico che il volto trovato sia delle dimensioni richieste
                if fh < 20 and fw < 20:
                    continue

                # Resize dell'immagine come rieschisto dal modello
                img = cv2.resize(roi, (96, 96))

                encoding = img_to_encoding(img)

                # Cerco il modello creato nel database
                for names in database:
                    # Cerco somiglianze usando la norma L2
                    dist = np.linalg.norm(np.subtract(database[names], encoding))
                    # Controllo se è la minima distanza
                    if dist < min_dist:
                        min_dist = dist
                        name = names
            # Se la distanza minima è minore del threshold allora posso aprire la porta
            if min_dist <= 0.4 and find:
                print(find)
                print("Porta sbloccata: bentornato " + str(name))
                break
            else:
                print("Porta non aperta. Invio della notifica in corso\n")
                cv2.imwrite("./Dataset/sconosciuto.jpg", frame)
                send_notification()
                from server import get_response
                while get_response() is None:
                    time.sleep(1)
                if str(get_response()) == "b'Apri la porta'":
                    print(get_response())
                    print("Accesso consentito\n")
                    break
                else:
                    print(get_response())
                    print("Accesso non consentito\n")
                    break
        # Attivo la webcam per 5 secondi
        if curr_time - start_time > 5:
            break

        cv2.waitKey(1)
        cv2.imshow("frame", frame)

    cap.release()
    cv2.destroyAllWindows()
    print(min_dist)


"""
    if len(face) == 0:
        print("Nessun volto trovato. Riprova\n")
        print(min_dist)
    elif len(face) > 1:
        print("Sono stati identificati più volti. Riprova\n")
        print(min_dist)
    elif min_dist > 0.4:
        print("Volto non riconosciuto. Riprova\n")
        print(min_dist)
"""


def send_notification():
    onesignal_client = onesignal.Client(app_auth_key="N2E4NTNkNzAtYjhjYi00ZTI0LWIzZWUtYTM1YmIyMmQxNzE4",
                                        app_id="1784a5bd-7107-4bda-b628-a19c2034159e")
    new_notification = onesignal.Notification(post_body={"contents": {"en": "Qualcuno ha suonato alla tua porta!"}})
    new_notification.post_body["included_segments"] = ["Active Users"]
    new_notification.post_body["headings"] = {"en": "Din Dong!"}
    onesignal_response = onesignal_client.send_notification(new_notification)

    print(onesignal_response.status_code)
    print(onesignal_response.json())


def delete_photo():
    if os.path.exists("./Dataset/sconosciuto.jpg"):
        os.remove("./Dataset/sconosciuto.jpg")


face_recognize()
delete_photo()
