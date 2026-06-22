import csv
import sqlite3
import json
import requests
import os

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_CSV = os.path.join(BASE_DIR, "data", "raw", "maneges.csv")
PROCESSED_CSV = os.path.join(BASE_DIR, "data", "processed", "donnees_maneges.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "maneges.db")
# --------------------------

def afficher_message_bienvenue():
    #Afficher un message de bienvenue à l'utilisateur.
    print("Bienvenue ! Nous allons charger les données sur les manèges.")

def charger_fichier_csv(fichier_csv):
    #Charger les lignes du fichier CSV.
    with open(fichier_csv, 'r', encoding='utf-8') as fichier:
        reader = csv.reader(fichier, delimiter=',', quotechar='"')
        return list(reader)

def selectionner_champs(donnees, champs_a_selectionner):
    #Sélectionner les champs désirés à partir des données.
    donnees_selectionnees = []
    for ligne in donnees[1:]:  # ignorer la première ligne (entête)
        champs = [ligne[i] for i in champs_a_selectionner]
        donnees_selectionnees.append(champs)
    return donnees_selectionnees

def enregistrer_donnees_selectionnees(fichier_destination, donnees_selectionnees):
    #Enregistrer les données sélectionnées dans un nouveau fichier CSV.
    with open(fichier_destination, 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier, delimiter=',', quotechar='"')
        writer.writerow(["Parc", "Type", "Ouvert", "Vitesse"])
        writer.writerows(donnees_selectionnees)

def charger_donnees_dans_sqlite(fichier_csv, nom_table, chemin_db):
    # Charger les données du fichier CSV dans la table SQLite.
    connexion = sqlite3.connect(chemin_db)
    curseur = connexion.cursor()

    # Créer la table si elle n'existe pas
    curseur.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            Parc TEXT,
            Type TEXT,
            Ouvert TEXT,
            Vitesse TEXT
        )
    '''.format(nom_table))

    # Lire les données du fichier CSV
    with open(fichier_csv, 'r', encoding='utf-8') as fichier:
        reader = csv.reader(fichier, delimiter=',', quotechar='"')
        next(reader)  # Ignorer la première ligne (entête)
        for ligne in reader:
            # Insérer les données dans la table
            curseur.execute('''
                INSERT INTO {} (Parc, Type, Ouvert, Vitesse)
                VALUES (?, ?, ?, ?)
            '''.format(nom_table), ligne)

    # Valider les modifications
    connexion.commit()

    # Fermer la connexion
    connexion.close()

def collecter_donnees_maneges():
    #Collecter les données des manèges à partir du serveur.
    url = "https://degenio.com/html5/manege_data.json"
    reponse = requests.get(url)
    if reponse.status_code == 200:
        donnees = json.loads(reponse.content)
        return donnees
    else:
        print("Erreur lors de la collecte des données")
        return None

def charger_donnees_maneges_dans_sqlite(donnees, nom_table, chemin_db):
    #Charger les données des manèges dans la table SQLite.
    connexion = sqlite3.connect(chemin_db)
    curseur = connexion.cursor()

    # Insérer les données dans la table
    for donnee in donnees:
        curseur.execute('''
            INSERT INTO {} (Parc, Type, Ouvert, Vitesse)
            VALUES (?, ?, ?, ?)
        '''.format(nom_table), (donnee['Parc'], donnee['Type'], donnee['Ouvert'], donnee['Vitesse']))

    # Valider les modifications
    connexion.commit()

    # Fermer la connexion
    connexion.close()

def main():
    afficher_message_bienvenue()

    print("\nÉtape 1 : Charger les données à partir d'un fichier CSV...")
    donnees = charger_fichier_csv(RAW_CSV)
    print("Données chargées avec succès !")

    champs_a_selectionner = [0, 1, 5, 6]
    donnees_selectionnees = selectionner_champs(donnees, champs_a_selectionner)

    print("\nÉtape 2 : Enregistrer les données sélectionnées dans un nouveau fichier CSV...")
    enregistrer_donnees_selectionnees(PROCESSED_CSV, donnees_selectionnees)
    print("Données enregistrées avec succès !")

    print("\nÉtape 3 : Charger les données dans la base de données SQLite...")
    nom_table = "maneges"
    charger_donnees_dans_sqlite(PROCESSED_CSV, nom_table, DB_PATH)
    print("Données chargées dans la base de données avec succès !")

    print("\nÉtape 4 : Collecter les données à partir de l'URL...")
    donnees_maneges = collecter_donnees_maneges()
    if donnees_maneges is not None:
        print("Données collectées avec succès !")
        print("\nÉtape 5 : Charger les données collectées dans la base de données SQLite...")
        charger_donnees_maneges_dans_sqlite(donnees_maneges, nom_table, DB_PATH)
        print("Données chargées dans la base de données avec succès !")
    else:
        print("Erreur lors de la collecte des données.")

if __name__ == "__main__":
    main()