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
