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
        
        # Récupérer le nom d'utilisateur
        self.player_name = master.username if hasattr(master, 'username') else "Joueur"

         # Connection DB
        self.conn = sqlite3.connect('blindtest_scores.db')
        self.cursor = self.conn.cursor()
        
        # Création de tables
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
       
        # Initialisation pygame mixer
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

    def load_songs_fr(self):
        # Données des chansons avec chemins et réponses possibles
        return [
            {
                "title": "Booba - Dolce Camara",
                "file": "./RAP_FR/Novice/Booba - Dolce Camara.mp3",
                "difficulty": "Novice",
                "answers": ["booba dolce camara", "dolce camara", "booba","b2o"]
            },
            {
                "title": "Booba - Freestyle CKO",
                "file": "./RAP_FR/Novice/Booba - Freestyle CKO.mp3",
                "difficulty": "Novice",
                "answers": ["booba freestyle cko", "freestyle cko", "booba","b2o"]
            },
            {
                "title": "Booba ft. Kaaris - Kalash",
                "file": "./RAP_FR/Novice/Booba ft. Kaaris - Kalash.mp3",
                "difficulty": "Novice",
                "answers": ["booba kalash", "kalash", "booba","kaaris","k2a","b2o"]
            },
            {
                "title": "Gazo - Probation",
                "file": "./RAP_FR/Novice/Gazo - Probation.mp3",
                "difficulty": "Novice",
                "answers": ["gazo probation", "probation", "gazo","bsb"]
            },
            {
                "title": "Gazo & Tiakola - Cartier",
                "file": "./RAP_FR/Novice/Gazo & Tiakola - Cartier.mp3",
                "difficulty": "Novice",
                "answers": ["gazo cartier", "cartier", "gazo","tiakola","tiako","la melo","bsb"]
            },
            {
                "title": "Genezio ft. La Mano 1.9 - EL GEMANO",
                "file": "./RAP_FR/Novice/Genezio ft. La Mano 1.9 - EL GEMANO.mp3",
                "difficulty": "Novice",
                "answers": ["genezio el gemano", "el gemano", "genezio","la mano"]
            },
            {
                "title": "Genezio ft. Tiakola - La melo est dans le bounce",
                "file": "./RAP_FR/Novice/Genezio ft. Tiakola - La melo est dans le bounce.mp3",
                "difficulty": "Novice",
                "answers": ["genezio la melo est dans le bounce", "la melo est dans le bounce", "genezio", "tiakola","la melo","tiako"]
            },
            {
                "title": "Gims ft. Dystinct - SPIDER",
                "file": "./RAP_FR/Novice/Gims ft. Dystinct - SPIDER.mp3",
                "difficulty": "Novice",
                "answers": ["gims spider", "spider", "gims","dystinct"]
            },
            {
                "title": "Guy2Bezbar - Monaco",
                "file": "./RAP_FR/Novice/Guy2Bezbar - Monaco.mp3",
                "difficulty": "Novice",
                "answers": ["guy2bezbar monaco", "monaco", "guy2bezbar"]
            },
            {
                "title": "Heuss Lenfoire ft. Werenoi - Melanine",
                "file": "./RAP_FR/Novice/Heuss Lenfoire ft. Werenoi - Melanine.mp3",
                "difficulty": "Novice",
                "answers": ["heuss melanine", "melanine", "heuss", "werenoi","lenfoire"]
            },
            {
                "title": "Kalash Criminel - 10 12 14 bureau",
                "file": "./RAP_FR/Novice/Kalash Criminel - 10 12 14 bureau.mp3",
                "difficulty": "Novice",
                "answers": ["kalash criminel 10 12 14 bureau", "10 12 14 bureau", "kalash criminel","crimi"]
            },
            {
                "title": "La Mano 1.9 ft. Niska - Canon",
                "file": "./RAP_FR/Novice/La Mano 1.9 ft. Niska - Canon.mp3",
                "difficulty": "Novice",
                "answers": ["la mano canon", "canon", "la mano","niska"]
            },
            {
                "title": "Ninho - 25G",
                "file": "./RAP_FR/Novice/Ninho - 25G.mp3",
                "difficulty": "Novice",
                "answers": ["ninho 25g", "25g", "ninho","NI"]
            },
            {
                "title": "Ninho ft. Niska - Coco",
                "file": "./RAP_FR/Novice/Ninho ft. Niska - Coco.mp3",
                "difficulty": "Novice",
                "answers": ["ninho coco", "coco", "ninho","niska","NI"]
            },
            {
                "title": "Niska & Ninho ft. Koba LaD - 911",
                "file": "./RAP_FR/Novice/Niska & Ninho ft. Koba LaD - 911.mp3",
                "difficulty": "Novice",
                "answers": ["niska ninho 911", "911", "niska","ninho","koba","lad","NI"]
            },
            {
                "title": "Squadra ft. Landy - En bas de chez moi",
                "file": "./RAP_FR/Novice/Squadra ft. Landy - En bas de chez moi.mp3",
                "difficulty": "Novice",
                "answers": ["squadra en bas de chez moi", "en bas de chez moi", "squadra","landy"]
            },
            {
                "title": "Timal ft. Gazo - Filtré",
                "file": "./RAP_FR/Novice/Timal ft. Gazo - Filtré.mp3",
                "difficulty": "Novice",
                "answers": ["timal filtré", "filtré", "timal","gazo"]
            },
            {
                "title": "Werenoi - Laboratoire",
                "file": "./RAP_FR/Novice/Werenoi - Laboratoire.mp3",
                "difficulty": "Novice",
                "answers": ["werenoi laboratoire", "laboratoire", "werenoi"]
            },
            {
                "title": "Werenoi ft. Damso - Pyramide",
                "file": "./RAP_FR/Novice/Werenoi ft. Damso - Pyramide.mp3",
                "difficulty": "Novice",
                "answers": ["werenoi pyramide", "pyramide", "werenoi","damso"]
            },
            {
                "title": "Werenoi ft. SDM - Dans un verre",
                "file": "./RAP_FR/Novice/Werenoi ft. SDM - Dans un verre.mp3",
                "difficulty": "Novice",
                "answers": ["werenoi dans un verre", "dans un verre", "werenoi","sdm"]
            },
            {
                "title": "Gazo - Nanani nanana",
                "file": "./RAP_FR/Intermediaire/Gazo - Nanani nanana.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["gazo nanani nanana", "nanani nanana", "gazo"]
            },
            {
                "title": "Genezio ft. Landy - Enfant du ghetto",
                "file": "./RAP_FR/Intermediaire/Genezio ft. Landy - Enfant du ghetto.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["genezio enfant du ghetto", "enfant du ghetto", "genezio","landy"]
            },
            {
                "title": "Guy2Bezbar - Mon année",
                "file": "./RAP_FR/Intermediaire/Guy2Bezbar - Mon année.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["guy2bezbar mon année", "mon année", "guy2bezbar"]
            },
            {
                "title": "Ninho ft. Werenoi - 3 Singes",
                "file": "./RAP_FR/Intermediaire/Ninho ft. Werenoi - 3 Singes.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["ninho 3 singes", "3 singes", "ninho werenoi","ninho","werenoi"]
            },
            {
                "title": "Skima - Krieg Part.1 (TMAX)",
                "file": "./RAP_FR/Intermediaire/Skima - Krieg Part.1 (TMAX).mp3",
                "difficulty": "Intermédiaire",
                "answers": ["krieg", "krieg part 1", "skima","tmax"]
            },
            {
                "title": "Soolking ft. Gims - Carré Ok",
                "file": "./RAP_FR/Intermediaire/Soolking ft. Gims - Carré Ok.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["soolking carré ok", "carré ok", "soolking gims","gims","soolking"]
            },
            {
                "title": "Suprême NTM - Seine Saint-Denis Style",
                "file": "./RAP_FR/Intermediaire/Suprême NTM - Seine Saint-Denis Style.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["ntm seine saint denis style", "seine saint denis style", "supreme ntm","ntm","supreme"]
            },
            {
                "title": "Suprême NTM ft. Lord Kossity - Ma Benz",
                "file": "./RAP_FR/Intermediaire/Suprême NTM ft. Lord Kossity - Ma Benz.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["ntm ma benz", "ma benz", "supreme ntm","benz","ntm","supreme"]
            },
            {
                "title": "Werenoi - 3x filtré",
                "file": "./RAP_FR/Intermediaire/Werenoi - 3x filtré.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["werenoi 3x filtré", "3x filtré", "werenoi","3f"]
            },
            {
                "title": "Werenoi - Balmain",
                "file": "./RAP_FR/Intermediaire/Werenoi - Balmain.mp3",
                "difficulty": "Intermédiaire",
                "answers": ["werenoi balmain", "balmain", "werenoi"]
            },
            {
                "title": "4keus - Moussa",
                "file": "./RAP_FR/Extreme/4keus - Moussa.mp3",
                "difficulty": "Extrême",
                "answers": ["4keus moussa", "moussa", "4keus"]
            },
            {
                "title": "Gradur - Terraser",
                "file": "./RAP_FR/Extreme/Gradur - Terraser.mp3",
                "difficulty": "Extrême",
                "answers": ["gradur terraser", "terraser", "gradur"]
            },
            {
                "title": "Kaaris - Zoo",
                "file": "./RAP_FR/Extreme/Kaaris - Zoo.mp3",
                "difficulty": "Extrême",
                "answers": ["kaaris zoo", "zoo", "kaaris","k2a"]
            },
            {
                "title": "Ninho - Binks To Binks 2",
                "file": "./RAP_FR/Extreme/Ninho - Binks To Binks 2.mp3",
                "difficulty": "Extrême",
                "answers": ["ninho binks to binks 2", "binks to binks 2", "ninho","ni"]
            },
            {
                "title": "SCH - Champs Élysées",
                "file": "./RAP_FR/Extreme/SCH - Champs Élysées.mp3",
                "difficulty": "Extrême",
                "answers": ["sch champs élysées", "champs élysées", "sch"]
            },
        ]


    def show_genre_selection(self):
        self.clear_window()

        main_frame = tk.Frame(self.master, bg="#1A1A1A")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(
            main_frame,
            text="Choisissez un genre de Rap :",
            font=("Arial", 24, "bold"),
            fg="#FFD700",
            bg="#1A1A1A"
        )
        title_label.pack(pady=30)

        for genre in self.genres.keys():
            btn = tk.Button(
                main_frame,
                text=genre,
                command=lambda g=genre: self.select_genre(g),
                width=20,
                height=2,
                font=("Arial", 12, "bold"),
                bg="#4B0082",
                fg="white",
                relief="raised",
                cursor="hand2"
            )
            btn.pack(pady=10)
        
        leaderboard_button = tk.Button(
            main_frame,
            text="Leaderboard",
            command=self.show_leaderboard,
            width=20,
            height=2,
            font=("Arial", 12, "bold"),
            bg="#4B0082",
            fg="white",
            relief="raised",
            cursor="hand2"
        )
        leaderboard_button.pack(pady=10)

    def show_leaderboard(self):
        self.clear_window()
    
        self.master.configure(bg="#1A1A1A")
    
        back_button = tk.Button(
            self.master,
            text="← Retour",
            command=self.show_genre_selection,
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            relief="flat",
            cursor="hand2"
        )
        back_button.place(x=20, y=20)
    
        tk.Label(
            self.master,
            text="Meilleurs Scores",
            font=("Arial", 24, "bold"),
            fg="#FFD700",
            bg="#1A1A1A"
        ).pack(pady=20)
    
        scores_frame = tk.Frame(self.master, bg="#1A1A1A")
        scores_frame.pack(expand=True, fill="both", padx=20)
    
        headers = ["Joueur", "Genre", "Difficulté", "Score", "Date"]
        for i, header in enumerate(headers):
            tk.Label(
                scores_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg="#FFD700",
                bg="#1A1A1A"
            ).grid(row=0, column=i, padx=10, pady=5)
    
        self.cursor.execute('''
        SELECT player_name, genre, difficulty, score, date
        FROM leaderboard
        ORDER BY score DESC, difficulty DESC
        LIMIT 10
        ''')
    
        for row_idx, score in enumerate(self.cursor.fetchall(), 1):
            for col_idx, value in enumerate(score):
                tk.Label(
                    scores_frame,
                    text=str(value),
                    font=("Arial", 10),
                    fg="white",
                    bg="#1A1A1A"
                ).grid(row=row_idx, column=col_idx, padx=10, pady=5)

    def select_genre(self, genre):
        self.selected_genre = genre
        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        self.clear_window()

        self.master.configure(bg="#1A1A1A")

        self.back_button = tk.Button(
            self.master,
            text="← Retour",
            command=self.show_genre_selection,
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            relief="flat",
            cursor="hand2"
        )
        self.back_button.place(x=20, y=20)

        title_label = tk.Label(
            self.master,
            text="Choisissez une difficulté :",
            font=("Arial", 24, "bold"),
            fg="#FFD700",
            bg="#1A1A1A"
        )
        title_label.pack(pady=(150, 20))

        self.buttons_frame = tk.Frame(self.master, bg="#1A1A1A")
        self.buttons_frame.pack(expand=True)

        for difficulty in ["Novice", "Intermédiaire", "Extrême"]:
            btn = tk.Button(
                self.buttons_frame,
                text=difficulty,
                command=lambda d=difficulty: self.select_difficulty(d),
                width=20,
                height=2,
                font=("Arial", 12, "bold"),
                bg="#4B0082",
                fg="white",
                relief="raised",
                cursor="hand2"
            )
            btn.pack(pady=10)

    def select_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
        self.prepare_game()
        self.show_game_interface()

    def prepare_game(self):
        all_songs = [song for song in self.genres[self.selected_genre] if song["difficulty"] == self.selected_difficulty]
        num_songs = self.difficulties[self.selected_difficulty]["count"]
        self.current_playlist = random.sample(all_songs, min(num_songs, len(all_songs)))
        self.current_song_index = 0
        self.score = 0

    def show_game_interface(self):
        self.clear_window()

        self.master.configure(bg="#1A1A1A")

        container = tk.Frame(self.master, bg="#1A1A1A")
        container.pack(expand=True, fill="both")

        self.song_progress_label = tk.Label(
            container,
            text=f"Extrait {self.current_song_index + 1}/{len(self.current_playlist)}",
            font=("Arial", 14),
            fg="white",
            bg="#1A1A1A"
        )
        self.song_progress_label.pack(pady=10)

        self.play_button = tk.Button(
            container,
            text="Jouer l'extrait",
            command=self.play_music,
            font=("Arial", 12, "bold"),
            bg="#4B0082",
            fg="white",
            width=20,
            height=2,
            cursor="hand2"
        )
        self.play_button.pack(pady=20)

        self.answer_entry = tk.Entry(
            container,
            width=50,
            font=("Arial", 12),
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        self.answer_entry.pack(pady=20)

        self.submit_button = tk.Button(
            container,
            text="Valider",
            command=self.check_answer,
            font=("Arial", 12, "bold"),
            bg="#4B0082",
            fg="white",
            width=15,
            cursor="hand2"
        )
        self.submit_button.pack(pady=10)

        self.timer_canvas = tk.Canvas(container, width=400, height=30, bg="#333333", highlightthickness=0)
        self.timer_canvas.pack(pady=10)

        self.timer_bar = self.timer_canvas.create_rectangle(0, 0, 0, 30, fill="green", width=0)

        self.score_label = tk.Label(
            container,
            text=f"Score : {self.score}",
            font=("Arial", 16, "bold"),
            fg="#FFD700",
            bg="#1A1A1A"
        )
        self.score_label.pack(pady=20)

    def play_music(self):
        if not self.is_playing and self.current_song_index < len(self.current_playlist):
            self.is_playing = True
            # Désactiver le bouton Valider pendant la lecture
            self.submit_button.configure(state='disabled')
            pygame.mixer.music.load(self.current_playlist[self.current_song_index]["file"])
            pygame.mixer.music.play()
            duration = self.difficulties[self.selected_difficulty]["duration"]
            self.start_timer(duration)


    def stop_music(self):
        pygame.mixer.music.stop()

    def start_timer(self, duration):
        self.remaining_time = duration
        self.update_timer_bar(duration)

    def update_timer_bar(self, duration):
        if self.remaining_time > 0:
            proportion = (duration - self.remaining_time) / duration
            color = self.get_color(proportion)
            width = 400 * proportion
            self.timer_canvas.coords(self.timer_bar, 0, 0, width, 30)
            self.timer_canvas.itemconfig(self.timer_bar, fill=color)
            
            self.remaining_time -= 1
            self.master.after(1000, lambda: self.update_timer_bar(duration))
        else:
            self.stop_music()
            self.timer_canvas.coords(self.timer_bar, 0, 0, 400, 30)
            self.timer_canvas.itemconfig(self.timer_bar, fill="#FF0000")
            
            # Appeler automatiquement la méthode check_answer
            self.check_answer()

            # Désactiver le bouton valider pendant les 2 dernières secondes
            if self.remaining_time <= 2:
                self.submit_button.configure(state='disabled')

            # Réactiver le bouton Valider
            self.submit_button.configure(state='normal')

            # Réinitialiser l'état de lecture pour permettre de passer à l'extrait suivant
            self.is_playing = False
            
    def get_color(self, proportion):
        if proportion < 0.5:
            return "#00FF00"  # Vert
        elif proportion < 0.8:
            return "#FFA500"  # Orange
        else:
            return "#FF0000"  # Rouge

    def check_answer(self):
        self.stop_music()
        # Arrêter et réinitialiser la barre de progression
        self.remaining_time = 0
        self.timer_canvas.coords(self.timer_bar, 0, 0, 0, 30)
        self.timer_canvas.itemconfig(self.timer_bar, fill="#00FF00")
        self.is_playing = False
        
        user_answer = self.answer_entry.get().strip().lower()
        correct_answers = [ans.lower() for ans in self.current_playlist[self.current_song_index]["answers"]]

        if any(user_answer == answer for answer in correct_answers):
            # Attribution des points selon la difficulté
            if self.selected_difficulty == "Novice":
                self.score += 1
            elif self.selected_difficulty == "Intermédiaire":
                self.score += 3
            elif self.selected_difficulty == "Extrême":
                self.score += 5
            messagebox.showinfo("Correct!", "Bonne réponse!")
        else:
            correct_answer_display = ", ".join(self.current_playlist[self.current_song_index]["answers"])
            messagebox.showinfo("Incorrect", f"La bonne réponse était : {correct_answer_display}")

        self.current_song_index += 1
        if self.current_song_index < len(self.current_playlist):
            self.song_progress_label.config(text=f"Extrait {self.current_song_index + 1}/{len(self.current_playlist)}")
            self.answer_entry.delete(0, tk.END)
        else:
            self.show_final_score()



    def show_final_score(self):
        self.clear_window()
        self.save_score()
        
        final_frame = tk.Frame(self.master, bg="#1A1A1A")
        final_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            final_frame,
            text=f"Score final : {self.score}",
            font=("Arial", 24, "bold"),
            fg="#FFD700",
            bg="#1A1A1A"
        ).pack(pady=20)
        
        tk.Label(
            final_frame,
            text=f"Merci d'avoir joué, {self.player_name}!",
            font=("Arial", 18),
            fg="white",
            bg="#1A1A1A"
        ).pack(pady=10)
        
        tk.Button(
            final_frame,
            text="Rejouer",
            command=self.show_genre_selection,
            font=("Arial", 14, "bold"),
            bg="#4B0082",
            fg="white"
        ).pack(pady=10)
        
        tk.Button(
            final_frame,
            text="Voir le Leaderboard",
            command=self.show_leaderboard,
            font=("Arial", 14, "bold"),
            bg="#4B0082",
            fg="white"
        ).pack(pady=10)


    def save_score(self):
        self.cursor.execute('''
        INSERT INTO leaderboard (player_name, genre, difficulty, score, total_songs, date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.player_name,
            self.selected_genre,
            self.selected_difficulty,
            self.score,
            len(self.current_playlist),
            datetime.now()
        ))
        self.conn.commit()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# Code pour lancer l'application
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()