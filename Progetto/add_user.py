import cv2
from scipy.io.wavfile import write
import sounddevice as sd


def init_camera():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    return cam

def add_user():
    cam = init_camera()
    face_detector = cv2.CascadeClassifier('CascadeClassifier/haarcascade_frontalface_default.xml')

    # Per ogni persona, inserisco un id numerico
    face_id = input('\n Inserisci id utente: ')
    print("\nInizializzazione. Attendere prego...")

    count = 0
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.2, 8)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1

            # Salvo l'immagine nella cartella dataset
            cv2.imwrite("Dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
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

    print("Parla")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('./Registrazioni/input' + str(face_id) + '.wav', fs, myrecording)
    print("Registrazione terminata con successo")

init_camera()
add_user()



