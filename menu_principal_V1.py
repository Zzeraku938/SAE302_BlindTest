import tkinter as tk
import pygame
import random

class BlindtestInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Blindtest Musical")
        self.master.geometry("500x400")

        pygame.mixer.init()
