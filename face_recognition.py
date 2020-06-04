import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Trainer/trainer.yml')
cascadePath = "CascadeClassifier/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

# Nome associato all'ID
names = ['Sconosciuto', 'Amedeo', 'Enzo']

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