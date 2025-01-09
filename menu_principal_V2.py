import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pygame
import random
import sqlite3
import hashlib
from datetime import datetime

def init_database():
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
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaderboard (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        genre TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_songs INTEGER NOT NULL,
        date DATETIME NOT NULL
    )''')
    
    conn.commit()
    return conn, cursor

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def inscrire_utilisateur(cursor, nom, prenom, nom_utilisateur, email, mot_de_passe):
    try:
        hashed_password = hash_password(mot_de_passe)
        cursor.execute('''
        INSERT INTO utilisateurs (nom, prenom, nom_utilisateur, email, mot_de_passe)
        VALUES (?, ?, ?, ?, ?)''', (nom, prenom, nom_utilisateur, email, hashed_password))
        return True
    except sqlite3.IntegrityError:
        return False

def connecter_utilisateur(cursor, nom_utilisateur, mot_de_passe):
    hashed_password = hash_password(mot_de_passe)
    cursor.execute('''
    SELECT * FROM utilisateurs WHERE nom_utilisateur = ? AND mot_de_passe = ?''', (nom_utilisateur, hashed_password))
    return cursor.fetchone() is not None

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Blindtest Musical")
        self.geometry("500x550")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.conn, self.cursor = init_database()
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
        
        if connecter_utilisateur(self.master.cursor, username, password):
            print("Connexion réussie")
            # Créer une nouvelle fenêtre pour le jeu
            game_window = tk.Tk()
            game_window.username = username
            game = BlindtestGame(game_window)
            self.master.withdraw()  # Cache la fenêtre de connexion au lieu de la détruire
            game_window.protocol("WM_DELETE_WINDOW", lambda: self.quit_game(game_window))
            game_window.mainloop()
            return
        
        print("Identifiants / Mot de passe incorrects")

    def quit_game(self, game_window):
        game_window.destroy()
        self.master.destroy()

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

    def register(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        
        password = self.password_entry.get()
        
        if password != self.confirm_password_entry.get():
            print("Les mots de passe ne correspondent pas")
            return
        
        if inscrire_utilisateur(self.master.cursor, lastname, firstname, username, email, password):
            print("Inscription réussie")
            # Créer une nouvelle fenêtre pour le jeu
            game_window = tk.Tk()
            game_window.username = username
            game = BlindtestGame(game_window)
            self.master.withdraw()  # Cache la fenêtre d'inscription au lieu de la détruire
            game_window.protocol("WM_DELETE_WINDOW", lambda: self.quit_game(game_window))
            game_window.mainloop()
            return
        
        print("Erreur lors de l'inscription")

    def quit_game(self, game_window):
        game_window.destroy()
        self.master.destroy()
       

class BlindtestGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blindtest Musical")
        self.master.geometry("800x600")
        self.master.configure(bg="#1A1A1A")
        
        # Ajouter cette ligne pour récupérer le nom d'utilisateur
        self.player_name = master.username if hasattr(master, 'username') else "Joueur"

         # Initialize database connection
        self.conn = sqlite3.connect('blindtest_scores.db')
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            genre TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_songs INTEGER NOT NULL,
            date DATETIME NOT NULL
        )''')
        self.conn.commit()

        # Initialisation directe de la base de données dans __init__
        self.conn = sqlite3.connect('blindtest_users.db')
        self.cursor = self.conn.cursor()

        # Création de la table si elle n'existe pas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            genre TEXT NOT NULL, 
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_songs INTEGER NOT NULL,
            date DATETIME NOT NULL
        )''')
        self.conn.commit()
       
        # Initialize pygame mixer
        pygame.mixer.init()

        # Chansons avec plusieurs réponses possibles
        self.genres = {
            "RAP FR": self.load_songs_fr(),
            "RAP US": []  # Ajoute ici des chansons pour RAP US si nécessaire
        }

        self.difficulties = {
            "Novice": {"count": 20, "duration": 30},
            "Intermédiaire": {"count": 10, "duration": 20},
            "Extrême": {"count": 5, "duration": 10}
        }

        self.selected_genre = None
        self.selected_difficulty = None
        self.current_playlist = []
        self.current_song_index = 0
        self.score = 0
        self.timer = None
        self.is_playing = False
        self.remaining_time = 0
        
        # Afficher directement le menu de sélection des genres
        self.show_genre_selection()

    def start_game(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showerror("Erreur", "Veuillez entrer un nom")
            return
        self.show_genre_selection()
