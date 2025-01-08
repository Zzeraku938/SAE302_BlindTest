import tkinter as tk
import pygame
import random

class BlindtestInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Blindtest Musical")
        self.master.geometry("500x400")

        pygame.mixer.init()

        self.genres = {
            "RAP FR": [
                {"title": "Chanson RAP FR 1", "file": "chemin/vers/rap_fr_1.mp3"},
                {"title": "Chanson RAP FR 2", "file": "chemin/vers/rap_fr_2.mp3"},
            ],
            "RAP US": [
                {"title": "Chanson RAP US 1", "file": "chemin/vers/rap_us_1.mp3"},
                {"title": "Chanson RAP US 2", "file": "chemin/vers/rap_us_2.mp3"},
            ],
            "Latino": [
                {"title": "Chanson Latino 1", "file": "chemin/vers/latino_1.mp3"},
                {"title": "Chanson Latino 2", "file": "chemin/vers/latino_2.mp3"},
            ],
            "Bouyon": [
                {"title": "Chanson Bouyon 1", "file": "chemin/vers/bouyon_1.mp3"},
                {"title": "Chanson Bouyon 2", "file": "chemin/vers/bouyon_2.mp3"},
            ],
            "Variété FR": [
                {"title": "Chanson Variété FR 1", "file": "chemin/vers/variete_fr_1.mp3"},
                {"title": "Chanson Variété FR 2", "file": "chemin/vers/variete_fr_2.mp3"},
            ]
        }

        self.selected_genre = None
        self.current_song = None
        self.score = 0

        self.genre_label = tk.Label(self.master, text="Choisissez un genre musical :", font=("Arial", 18))
        self.genre_label.pack(pady=20)

        self.genre_var = tk.StringVar(value="RAP FR")
        for genre in self.genres.keys():
            rb = tk.Radiobutton(self.master, text=genre, variable=self.genre_var, value=genre, command=self.select_genre)
            rb.pack(anchor=tk.W)

        self.play_button = tk.Button(self.master, text="Jouer l'extrait", command=self.play_music)
        self.play_button.pack(pady=10)

        self.answer_entry = tk.Entry(self.master, width=50)
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(self.master, text="Valider", command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.score_label = tk.Label(self.master, text="Score : 0", font=("Arial", 16))
        self.score_label.pack(pady=20)

    def select_genre(self):
        genre_name = self.genre_var.get()
        self.current_song = random.choice(self.genres[genre_name])
        print(f"Genre sélectionné : {genre_name}. Chanson actuelle : {self.current_song['title']}")

    def play_music(self):
        if self.current_song:
            pygame.mixer.music.load(self.current_song["file"])
            pygame.mixer.music.play()

    def check_answer(self):
        user_answer = self.answer_entry.get().lower()
        if self.current_song and user_answer == self.current_song["title"].lower():
            self.score += 1
            self.score_label.config(text=f"Score : {self.score}")
            self.answer_entry.delete(0, tk.END)
            # Sélectionner une nouvelle chanson après une bonne réponse
            self.select_genre()
        else:
            tk.messagebox.showinfo("Incorrect", "Essayez encore !")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlindtestInterface(root)
    root.mainloop()