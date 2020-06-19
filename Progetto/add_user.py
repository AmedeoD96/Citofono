import cv2
from scipy.io.wavfile import write
import sounddevice as sd
import fileinput
from cv2 import *
import time
import os
import pickle
from face_trainer import *
import noisereduce as nr
from scipy.io import wavfile
import librosa


def init_camera():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    return cam


def add_user():
    print("\nAvvio della fase di raccolta dati\n")
    cam = init_camera()
    face_detector = cv2.CascadeClassifier('CascadeClassifier/haarcascade_frontalface_default.xml')

    db_path = "./Dataset/embeddings.pickle"
    name = input("\n Inserisci il nome dell'utente: ")

    # Se il database non esiste, lo creo
    if os.path.exists(db_path):
        with open(db_path, 'rb') as database:
            db = pickle.load(database)

            if name in db or name == "Sconosciuto":
                print("Nome già presente nel db. Prova con un altro nome.\n")
                return
    else:
        # Se il db non esiste, ne creo uno nuovo
        db = {}

    print("\nInizializzazione. Attendere prego...")
    i = 3
    face_found = False

    while True:
        _, frame = cam.read()
        cv2.putText(frame, 'Inquadra il tuo volto', (100, 200), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)

        cv2.putText(frame, 'Avvio', (260, 270), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)

        cv2.putText(frame, str(i), (290, 330), cv2.FONT_HERSHEY_SIMPLEX,
                    1.3, (255, 255, 255), 3)

        i -= 1
        cv2.imshow('frame', frame)
        cv2.waitKey(1000)
        if i < 0:
            break

    start_time = time.time()

    # Face recognition
    while True:
        curr_time = time.time()
        _, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_detector.detectMultiScale(gray, 1.05, 8)
        if len(face) == 1:
            for (x, y, w, h) in face:
                # Considero solo il roi (Region Of Interest) dell'immagine
                roi = frame[y - 10:y + h + 10, x - 10:x + w + 10]
                fh, fw = roi.shape[:2]

                # Verifico che il volto trovato sia della grandezza minima richiesta
                if fh < 20 and fw < 20:
                    continue

                face_found = True
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 200, 200), 2)

        if curr_time - start_time >= 5:
            break

        cv2.imshow('frame', frame)
        cv2.waitKey(1)

    cam.release()
    cv2.destroyAllWindows()

    if face_found:
        img = cv2.resize(roi, (96, 96))
        db[name] = img_to_encoding(img)
        with open(db_path, "wb") as database:
            pickle.dump(db, database, protocol=pickle.HIGHEST_PROTOCOL)
    elif len(face) > 1:
        print("Sono state identificati più volti. Riprova\n")
        return
    else:
        print("Nessun volto trovato. Riprova\n")
        return

    # Acquisizione Audio utente
    fs = 44100
    seconds = 5

    print("Acquisizione volto completata.\nAvvio acquisizione audio\n")

    numero_wav = 3
    numero_audio_totale = 3
    audio = 0
    i = 0
    while audio < numero_wav:
        print("Immissione audio numero", str(i + 1))
        for j in range(3, 0, -1):
            print(f"La registrazione inizia tra {j}")
            time.sleep(1)
        print("Parla")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write('./Registrazioni/' + name + str(i + 1) + '.wav', fs, myrecording)
        print("Registrazione terminata con successo")
        audio += 1
        i += 1
        if audio == numero_wav:
            confirm = input('\nSe vuoi, puoi registare altri file audio per migliorare il riconoscimento.'
                            '\nPremi y se vuoi registrare altri file audio.'
                            '\nPremi n se non vuoi registrare altri file.')
            print(confirm)
            if confirm == 'y':
                numero_wav = int(input('\n Inserisci il numero di audio che vuoi generare: '))
                audio = 0
                numero_audio_totale = numero_audio_totale + numero_wav
    print("\nFase di raccolta dati terminata\n")
