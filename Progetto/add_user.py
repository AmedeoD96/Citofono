import cv2
from scipy.io.wavfile import write
import sounddevice as sd
import fileinput
import user_list
from cv2 import *


def init_camera():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    return cam


def get_count():
    file = open("count.txt", "r")
    count = file.readline().strip()
    return count


def update_counter_file():
    count = get_count()
    count = int(count)
    count += 1
    with fileinput.FileInput("count.txt", inplace=True, backup='.bak') as file:
        line = file.readline().strip()
        print(line.replace(line, str(count)), end='')


def add_user():
    cam = init_camera()
    face_detector = cv2.CascadeClassifier('CascadeClassifier/haarcascade_frontalface_default.xml')

    # Per ogni persona, inserisco un id numerico
    name = input("\n Inserisci il nome dell'utente: ")
    user_list.nuovo_utente(name)
    print("\nInizializzazione. Attendere prego...")

    count = 0
    while (True):
        ret, img = cam.read()
        if (ret):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.2, 8)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

            # Salvo l'immagine nella cartella dataset
                cv2.imwrite("Dataset/User." + str(get_count()) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
                cv2.imshow('image', img)
            k = cv2.waitKey(100) & 0xff  # ESC per uscire
            if k == 27:
                break
            elif count >= 30:  # Prendo 30 foto come esempio e poi stoppo il video
                break

    cam.release()
    cv2.destroyAllWindows()

    #  Acquisizione Audio utente
    fs = 44100
    seconds = 5

    numero_wav = input('\n Inserisci il numero di audio che vuoi generare: ')
    for i in range(0, int(numero_wav)):
        print("immissione audio numero", str(i + 1))
        print("Parla")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write('./Registrazioni/input' + str(i + 1) + '.wav', fs, myrecording)
    print("Registrazione terminata con successo")


init_camera()
add_user()
update_counter_file()
