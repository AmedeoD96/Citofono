import os

def nuovo_utente(nome):
    file = open("username.txt", "a+")
    if os.stat("username.txt").st_size == 0:
        file.writelines(nome)
    else:
        file.writelines("\n" + nome)
    file.close()
