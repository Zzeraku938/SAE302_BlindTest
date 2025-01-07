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

        self.register_button = ctk.CTkButton(self, text="S'inscrire", command=self.register)
        self.register_button.pack(pady=20)

        self.login_link = ctk.CTkButton(self, text="Déjà inscrit ? Se connecter", command=self.open_login)
        self.login_link.pack(pady=10)
        
   def register(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Ici, vous pouvez ajouter la logique de vérification et d'enregistrement
        if password != confirm_password:
            print("Les mots de passe ne correspondent pas")
        else:
            print(f"Tentative d'inscription pour : {username}")
            # Ajoutez ici le code pour enregistrer l'utilisateur dans votre base de données

if __name__ == "__main__":
    app = RegisterWindow()
    app.mainloop()