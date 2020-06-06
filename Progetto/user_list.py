def nuovo_utente(nome):
    file = open("username.txt", "a+")
    file.writelines(nome + "\r\n")
    file.close()
