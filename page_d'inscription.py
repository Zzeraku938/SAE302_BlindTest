import customtkinter as ctk

class RegisterWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inscription Blindtest Musical")
        self.geometry("500x550")

        # Configuration du thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Création des widgets
        self.label = ctk.CTkLabel(self, text="Inscription au Blindtest Musical", font=("Arial", 20))
        self.label.pack(pady=20)

        self.firstname_entry = ctk.CTkEntry(self, placeholder_text="Prénom")
        self.firstname_entry.pack(pady=15)

        self.lastname_entry = ctk.CTkEntry(self, placeholder_text="Nom")
        self.lastname_entry.pack(pady=15)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom d'utilisateur")
        self.username_entry.pack(pady=15)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Adresse Mail")
        self.email_entry.pack(pady=15)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=15)

        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirmer Mot de passe", show="*")
        self.confirm_password_entry.pack(pady=15)

if __name__ == "__main__":
    app = RegisterWindow()
    app.mainloop()