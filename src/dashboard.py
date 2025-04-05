# -*- coding: utf-8 -*-
#   dashboard.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |---------------Fenêtre de bord--------------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from comptes import calcul_dict_soldes, selection_compte
from import_donnees import import_comptes, import_operations
from shared import saisir_choix, dict_ident

# --Constantes-- #


# --Fonctions-- #
def fenetre_bord(identifiant: str) -> int:
    """
    Affiche un tableau de bord récapitulatif à l'utilisateur et lui propose de choisir la prochaine phase.

    Le tableau de bord affiche :
        - Le nom de l'utilisateur
        - Le solde du compte courant (défini via selection_compte())

    L'utilisateur peut ensuite choisir entre :
        - 0 : Se déconnecter
        - 1 : Accéder à la gestion des comptes
        - 2 : Accéder à la gestion des budgets

    Args:
        identifiant (int): Identifiant de l'utilisateur connecté, utilisé pour accéder à ses données personnelles.

    Returns:
        int: Le choix effectué par l'utilisateur (0, 1 ou 2)
    """
    cle_cryptage = dict_ident[identifiant][-1]
    lst_cpt = import_comptes(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    lst_ope = import_operations(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    dict_soldes = calcul_dict_soldes(lst_cpt, lst_ope)
    nom = dict_ident[identifiant][1]
    # selection_compte(lst_cpt) renvoie le compte courant, car courant=True par défaut
    solde_courant = dict_soldes[selection_compte(lst_cpt)]
    print(f"\n|-----Tableau de bord-----|\n"
          f"| Bonjour {nom} |\n"
          f"| Vous avez {solde_courant:.2f} € sur votre compte |")

    print("\nBienvenue. De quelle fonctionnalité avez-vous besoin ?")
    print("0. Déconnexion\n"
          "1. Gestion des comptes\n"
          "2. Gestion des budgets\n")

    return saisir_choix(valeurs_autorisees={0, 1, 2})

