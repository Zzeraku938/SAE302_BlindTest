import customtkinter as ctk

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Connexion Blindtest Musical")
        self.geometry("400x300")

        # Configuration du thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Création des widgets
        self.label = ctk.CTkLabel(self, text="Connexion au Blindtest Musical", font=("Arial", 20))
        self.label.pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom d'utilisateur")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Se connecter", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="S'inscrire", command=self.register)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Ici, vous pouvez ajouter la logique de vérification des identifiants
        print(f"Tentative de connexion : {username}")

    def register(self):
        # Ici, vous pouvez ajouter la logique pour l'inscription
        print("Ouverture de la page d'inscription")

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()