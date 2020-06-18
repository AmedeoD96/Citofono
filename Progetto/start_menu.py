def menu():
    print("""
    SmartRingbell
    1 - Aggiungi un nuovo utente
    2 - Modifica un utente
    3 - Suona il campanello
    4 - Elimina un utente
    5 - Esci dal Programma
    """)

    scelta = input()

    if scelta == 1:
        menu()
        # Aggiungi utente
    elif scelta == 2:
        # Elimina utente, poi fase di raccolta dati e infine di training
        menu()
    elif scelta == 3:
        # Start server, poi recognition
        menu()
    elif scelta == 4:
        # Delete user
        menu()
    elif scelta == 5:
        exit()


menu()
