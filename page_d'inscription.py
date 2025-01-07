import customtkinter as ctk

class RegisterWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inscription Blindtest Musical")
        self.geometry("500x550")

        # Configuration du thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = RegisterWindow()
    app.mainloop()