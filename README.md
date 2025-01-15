# SAE302_BlindTest

# Description du Projet

Application de blindtest musical spécialisée dans le rap français, permettant aux utilisateurs de tester leurs connaissances musicales à travers différents niveaux de difficulté.

# Fonctionnalités

~ Système d'authentification (inscription/connexion)
~ Sélection de genre musical (RAP FR)
3 niveaux de difficulté :
    - Novice : 20 extraits de 30 secondes
    - Intermédiaire : 10 extraits de 20 secondes
    - Extrême : 5 extraits de 10 secondes
~ Système de score avec leaderboard
~ Barre de progression temporelle
~ Validation flexible des réponses

# Prérequis

[python]

pip install tkinter
pip install pygame
pip install customtkinter
pip install sqlite3

# Structure des Dossiers

[text]

RAP_FR/
├── Novice/
│   └── (20 extraits musicaux)
├── Intermediaire/
│   └── (10 extraits musicaux)
└── Extreme/
    └── (5 extraits musicaux)
  
# Installation

1. Clonez le repository
2. Installez les dépendances requises
3. Assurez-vous que les chemins des fichiers audio sont correctement configurés
4. Lancez l'application avec python main.py

# Utilisation

1. Créez un compte ou connectez-vous
2. Sélectionnez le genre musical (RAP FR)
3. Choisissez votre niveau de difficulté
4. Écoutez les extraits et proposez vos réponses
5. Consultez votre score final et le leaderboard

# Fonctionnalités Techniques

~ Interface graphique avec Tkinter et CustomTkinter
~ Gestion audio avec Pygame
~ Base de données SQLite pour :
    - Gestion des utilisateurs
    - Stockage des scores
    - Classement des joueurs