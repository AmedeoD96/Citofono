def nuovo_utente(nome):
    file = open("username.txt", "a+")
    file.writelines("\n" + nome)
    file.close()