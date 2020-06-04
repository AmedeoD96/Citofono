import cv2
import os

cam = cv2.VideoCapture(0)
cam.set(3, 640) #larghezza
cam.set(4, 480) #altezza

face_detector = cv2.CascadeClassifier('CascadeClassifier/haarcascade_frontalface_default.xml')

#Per ogni persona, inserisco un id numerico
face_id = input('\n Inserisci id utente: ')
print("\nInizializzazione. Attendere prego...")

count = 0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1
        #Salvo l'immagine nella cartella dataset
        cv2.imwrite("Dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])
        cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff #ESC per uscire
    if k == 27:
        break
    elif count >= 30: #Prendo 30 foto come esempio e poi stoppo il video
        break

print("\n Uscita in corso...")
cam.release()
cv2.destroyAllWindows()
