import os

def removeGMM (nomeFile):
    if os.path.exists('./Trainer/model' + nomeFile + '.gmm'):
        os.remove('./Trainer/model' + nomeFile + '.gmm')
    print("rimozione modello avvenuta con successo")


