import os
import random

# Liste de prénoms (français + quelques origines diverses)
prenoms_mixes = [
    "Jean", "Marie", "Luc", "Claire", "Paul", "Julie",
    "Louis", "Camille", "Hugo", "Chloe", "Thomas", "Emma",
    "Youssef", "Nadia", "Amine", "Leila", "Ali", "Amina",
    "Zara", "Omar", "Imane", "Samir"
]


# Fonction pour générer un utilisateur
def generate_user_entry():
    identifiant = ''.join(random.choices('0123456789', k=8))
    mdp = ''.join(random.choices('0123456789', k=6))
    prenom = random.choice(prenoms_mixes)
    cle = f"{random.randint(1, 25):02d}"  # clé entre 01 et 25
    return f"{identifiant}*{mdp}*{prenom}*{cle}"


# Chemin du dossier de destination (modifie si besoin)
dossier_cible = os.path.join(os.getcwd(), "dossier_utilisateurs")
os.makedirs(dossier_cible, exist_ok=True)

# Génération et sauvegarde de 15 utilisateurs dans ident.txt (en UTF-8)
ident_file_path = os.path.join(dossier_cible, "ident.txt")
with open(ident_file_path, "w", encoding="utf-8") as f:
    for _ in range(15):
        f.write(generate_user_entry() + "\n")

print(f"[OK] Fichier ident.txt généré en UTF-8 dans : {ident_file_path}")
