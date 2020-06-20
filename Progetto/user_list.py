import pickle
import os


def get_user_list():
    db_path = "./Dataset/embeddings.pickle"
    if os.path.exists(db_path):
        database = pickle.load(open(db_path, "rb"))
        print("Gli utenti al momento registrati sono:\n")
        for names in database:
            print(names)
        print("\n")
    else:
        print("Nessun nome presente nel database")
