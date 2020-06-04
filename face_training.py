import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("CascadeClassifier/haarcascade_frontalface_default.xml")

# Acquisizione di immagini e labels
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
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

    return faceSamples, ids

print ("\n Fase di addestramento. Attendere...")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Salvo il modello
recognizer.write('Trainer/trainer.yml')

# Stampo il numero di facce imparate
print("\n [INFO] {0} Facce unoarate. Uscita in corso...".format(len(np.unique(ids))))