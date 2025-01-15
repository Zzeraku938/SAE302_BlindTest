import sqlite3
import hashlib
import customtkinter as ctk

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

def connecter_utilisateur(nom_utilisateur, mot_de_passe):
    hashed_password = hash_password(mot_de_passe)
    cursor.execute('''
    SELECT * FROM utilisateurs WHERE nom_utilisateur = ? AND mot_de passe = ?
    ''', (nom_utilisateur, hashed_password))
    utilisateur = cursor.fetchone()
    return utilisateur is not None


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Blindtest Musical")
        self.geometry("500x550")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.current_window = None
        self.show_login()
    
    def show_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = LoginWindow(self)
    
    def show_register(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = RegisterWindow(self)

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=ctk.BOTH, expand=True)

        self.label = ctk.CTkLabel(self, text="Connexion au Blindtest Musical", font=("Arial", 20))
        self.label.pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom d'utilisateur")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Se connecter", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="S'inscrire", command=self.master.show_register)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if connecter_utilisateur(username, password):
            print("Connexion réussie")
        else:
            print("Identifiants / Mot de passe incorrects")

class RegisterWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=ctk.BOTH, expand=True)

        self.label = ctk.CTkLabel(self, text="Inscription au Blindtest Musical", font=("Arial", 20))
        self.label.pack(pady=20)

        self.firstname_entry = ctk.CTkEntry(self, placeholder_text="Prénom")
        self.firstname_entry.pack(pady=10)

        self.lastname_entry = ctk.CTkEntry(self, placeholder_text="Nom")
        self.lastname_entry.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom d'utilisateur")
        self.username_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Adresse Mail")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=10)

        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirmer Mot de passe", show="*")
        self.confirm_password_entry.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="S'inscrire", command=self.register)
        self.register_button.pack(pady=20)

        self.login_link = ctk.CTkButton(self, text="Déjà inscrit ? Se connecter", command=self.master.show_login)
        self.login_link.pack(pady=10)

    def register(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            print("Les mots de passe ne correspondent pas")
        else:
            if inscrire_utilisateur(lastname, firstname, username, email, password):
                print("Inscription réussie")
                self.master.show_login()
            else:
                print("Erreur lors de l'inscription")
