import pickle
import os


# Elimino gli utenti registrati dal db
def delete_user():
    name = input("Inserisci il nome dell'utente: ")

    db_path = "./Dataset/embeddings.pickle"
    with open(db_path, "rb") as database:
        db = pickle.load(database)

    user = db.pop(name, None)

    if os.path.exists("./Trainer/model" + name + ".gmm"):
        os.remove("./Trainer/model" + name + ".gmm")

    if user is not None:
        print("Utente " + name + " eliminato con successo\n")
        # Salvo il db
        with open(db_path, "wb") as database:
            pickle.dump(db, database, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        print("Non c'è nessun utente con il nome " + name + " presente nel database\n")
