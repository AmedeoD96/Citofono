def menu():
    print("""
    SmartRingbell
    1 - Aggiungi un nuovo utente
    2 - Modifica un utente
    3 - Suona il campanello
    4 - Elimina un utente
    5 - Visualizza gli utenti registrati
    6 - Esci dal Programma
    """)

    scelta = input()

    if scelta == str(1):
        # Aggiungi utente
        from add_user import add_user
        add_user()
        from training import voice_model
        voice_model()
        menu()
    elif scelta == str(2):
        # Elimina utente, poi fase di raccolta dati e infine di training
        from delete_user import delete_user
        delete_user()
        from add_user import add_user
        add_user()
        from training import voice_model
        voice_model()
        menu()
    elif scelta == str(3):
        # Start server, poi recognition
        from recognition import face_recognize
        face_recognize()
        menu()
    elif scelta == str(4):
        # Delete user
        from delete_user import delete_user
        delete_user()
        menu()
    elif scelta == str(5):
        from user_list import get_user_list
        get_user_list()
    elif scelta == str(6):
        exit()


menu()
