import os
import random
from datetime import datetime, timedelta

# Comptes possibles
comptes_lettres = ["Compte A", "Compte B", "Compte C", "Compte D", "Compte E"]
comptes_speciaux = ["Compte Épargne", "Compte Enfant", "Compte Jeune", "Compte Salaire", "Compte Pro"]
libelles_depenses = ["cinema", "restaurant", "courses", "essence", "cadeau", "pharmacie"]
libelles_revenus = ["salaire", "remboursement", "virement", "revenu", "prime", "vente"]
types_ope = ["CB", "CHE", "VIR"]
budgets_possibles = ["sorties", "alimentation", "transport", "santé", "divertissement", "divers"]


def generate_comptes():
    nb_total = random.randint(1, 3)
    comptes = []

    # Ajoute des comptes lettres dans l'ordre (A, B, ...)
    nb_lettres = min(nb_total, len(comptes_lettres))
    comptes += comptes_lettres[:nb_lettres]

    # Complète avec des comptes spéciaux si besoin
    if nb_total > len(comptes):
        comptes += random.sample(comptes_speciaux, nb_total - len(comptes))

    return [f"CPT*{c}" for c in comptes]


def generate_operations(comptes):
    ops = []
    compte_labels = [cpt.split("*")[1] for cpt in comptes]
    nb_ope = random.randint(4, 20)
    nb_depenses = random.randint(int(nb_ope * 0.3), int(nb_ope * 0.6))
    nb_revenus = nb_ope - nb_depenses

    # Dépenses
    for _ in range(nb_depenses):
        date = (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 30))).strftime("%d/%m/%Y")
        lib = random.choice(libelles_depenses)
        compte = random.choice(compte_labels)
        montant = -round(random.uniform(5, 100), 2)
        type_ = random.choice(types_ope)
        verif = random.choice(["True", "False"])
        budget = random.choice(budgets_possibles)
        ops.append(f"OPE*{date}*{lib}*{compte}*{montant}*{type_}*{verif}*{budget}")

    # Revenus
    for _ in range(nb_revenus):
        date = (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 30))).strftime("%d/%m/%Y")
        lib = random.choice(libelles_revenus)
        compte = random.choice(compte_labels)
        montant = round(random.uniform(50, 300), 2)
        type_ = random.choice(types_ope)
        verif = random.choice(["True", "False"])
        budget = random.choice(budgets_possibles)
        ops.append(f"OPE*{date}*{lib}*{compte}*{montant}*{type_}*{verif}*{budget}")

    random.shuffle(ops)
    return ops


def generate_budgets(comptes):
    buds = ["BUD*Autres*0*Autres"]
    compte_labels = [cpt.split("*")[1] for cpt in comptes]
    nb_budgets = random.randint(1, 4)
    selected_budgets = random.sample(budgets_possibles, nb_budgets)
    for bud in selected_budgets:
        montant = random.choice([100, 200, 300, 500, 1000])
        compte = random.choice(compte_labels)
        buds.append(f"BUD*{bud}*{montant}*{compte}")
    return buds


# Dossier contenant ident.txt
base_dir = os.path.join(os.getcwd(), "dossier_utilisateurs")
ident_path = os.path.join(base_dir, "ident.txt")

# Dossier de sortie pour les fichiers utilisateurs
output_dir = os.path.join(base_dir, "users")
os.makedirs(output_dir, exist_ok=True)

# Lecture de ident.txt en UTF-8
with open(ident_path, "r", encoding="utf-8") as f:
    lignes = f.readlines()

# Génération des fichiers utilisateurs
for ligne in lignes:
    identifiant = ligne[:8]
    comptes = generate_comptes()
    operations = generate_operations(comptes)
    budgets = generate_budgets(comptes)

    contenu = "\n".join(comptes + operations + budgets)
    fichier_utilisateur = os.path.join(output_dir, f"{identifiant}.txt")

    with open(fichier_utilisateur, "w", encoding="utf-8") as f:
        f.write(contenu)

print(f"{len(lignes)} fichiers utilisateur générés dans le dossier : {output_dir}")
