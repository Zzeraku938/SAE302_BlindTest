import sqlite3
import hashlib

# Initialisation de la base de données
conn = sqlite3.connect('blindtest_users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    nom_utilisateur TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    mot_de_passe TEXT NOT NULL
)
''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def inscrire_utilisateur(nom, prenom, nom_utilisateur, email, mot_de_passe):
    try:
        hashed_password = hash_password(mot_de_passe)
        cursor.execute('''
        INSERT INTO utilisateurs (nom, prenom, nom_utilisateur, email, mot_de_passe)
        VALUES (?, ?, ?, ?, ?)
        ''', (nom, prenom, nom_utilisateur, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
