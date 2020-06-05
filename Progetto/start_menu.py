import add_user
# TODO finire
scelta = True

print("""
SmartRingbell
1 - Aggiungi un nuovo utente (in automatico verrà aggiornato il modello)
2 - Modifica un utente
3 - Avvia il riconoscimento
""")

scelta = input("Cosa vuoi fare?")

if scelta == 1:
    add_user.init_camera()
    add_user.add_user()
    exec(open("training.py").read())