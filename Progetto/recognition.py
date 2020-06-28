import os
import numpy as np
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import pickle
from sklearn import preprocessing
import librosa
import speaker_verification_toolkit.tools as svt
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import scale
import time
from face_trainer import *
import onesignal
import scipy.signal as sg
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
tf.get_logger().setLevel('ERROR')

def read_all_gmms():
    # Variabili riconoscimento voce
    models = []
    speakers = []
    find = False
    frequency_sample = 44100.0
    seconds = 3

    print("Avvio riconoscimento vocale: parla\n")
    myrecording = sd.rec(int(seconds * frequency_sample), samplerate=frequency_sample, channels=2)
    sd.wait()
    write('Registrazioni/input' + str(1000) + '.wav', frequency_sample, myrecording)

    data, sr = librosa.load('Registrazioni/input' + str(1000) + '.wav', sr=16000, mono=True)

    nyq = 0.5 * frequency_sample
    cutoff = 250
    normal_cutoff = cutoff / nyq
    numerator, denominator = sg.butter(1, normal_cutoff, 'low')
    data = sg.filtfilt(numerator, denominator, data)
    data = svt.rms_silence_filter(data)

    mfcc = svt.extract_mfcc(data, sr, winlen=0.025, winstep=0.01)
    mfcc = preprocessing.scale(mfcc)  # standardizza il dataset usando la standard scaler
    delta = librosa.feature.delta(mfcc)
    combined = np.hstack((mfcc, delta))

    basepath = "./Trainer"
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            if entry.endswith(".gmm"):
                gmm_readed = pickle.load(open(basepath + "/" + entry, 'rb'))
                speakers.append(entry)
                models.append(gmm_readed)

    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        # Calcola la probabilità su scala logaritmica per campione del parametro.
        # ritorna Log likelihood del Gaussian mixture dato il parametro combined.
        gmm = models[i]
        scores = np.array(gmm.score(combined))

        # Somma i valori di somiglianza per ogni campione
        log_likelihood[i] = scores.sum()

    # print(f"Log likelihood senza normalizzazione: {log_likelihood}")
    winner = np.argmax(log_likelihood)
    """
    print("i valori con la normalizzazione minmax")
    print(minmax_scale(log_likelihood))
    print("i valori con la normalizzazione scalescale")
    print(scale(log_likelihood))
    """
    trovato = log_likelihood
    if round(trovato[winner]) >= 59:
        print("Trovato\n")
        print(scale(log_likelihood))
        print(speakers[winner])
        find = True
    else:
        print("Non trovato\n")
        find = False

    if os.path.exists("./Registrazioni/input1000.wav"):
        os.remove("./Registrazioni/input1000.wav")
    log_likelihood = []
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
            if min_dist <= 0.52 and find:
                print(find)
                print("Porta sbloccata: bentornato " + str(name))
                send_notification(str(name) + " è tornato a casa")
                break
            elif min_dist <= 0.52 or find:
                handle_sconosciuto(frame, "Qualcuno è alla porta")
            else:
                handle_sconosciuto(frame, "Sconosciuto alla porta")

        # Attivo la webcam per 5 secondi
        if curr_time - start_time > 5:
            break

        cv2.waitKey(1)
        cv2.imshow("frame", frame)

    cap.release()
    cv2.destroyAllWindows()
    delete_photo()

    if len(face) == 0:
        print("Nessun volto trovato. Riprova\n")
    elif len(face) > 1:
        print("Sono stati identificati più volti. Riprova\n")


def send_notification(text):
    onesignal_client = onesignal.Client(app_auth_key="N2E4NTNkNzAtYjhjYi00ZTI0LWIzZWUtYTM1YmIyMmQxNzE4",
                                        app_id="1784a5bd-7107-4bda-b628-a19c2034159e")
    new_notification = onesignal.Notification(post_body={"contents": {"en": text}})
    new_notification.post_body["included_segments"] = ["Active Users"]
    new_notification.post_body["headings"] = {"en": "Din Dong!"}
    onesignal_client.send_notification(new_notification)


def handle_sconosciuto(frame, notification_message):
    print("Porta non aperta. Invio della notifica in corso\n")
    cv2.imwrite("./Dataset/sconosciuto.jpg", frame)
    send_notification(notification_message)
    while not os.path.exists("risposta.txt"):
        time.sleep(0.5)
    f = open("risposta.txt", "r")
    line = f.readline()
    f.close()
    if line == "Apri la Porta":
        print(line)
        print("Accesso consentito\n")
        if os.path.exists("risposta.txt"):
            os.remove("risposta.txt")
        return
    else:
        print(line)
        print("Accesso non consentito\n")
        if os.path.exists("risposta.txt"):
            os.remove("risposta.txt")
        return


def delete_photo():
    if os.path.exists("./Dataset/sconosciuto.jpg"):
        os.remove("./Dataset/sconosciuto.jpg")
