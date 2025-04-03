# -*- coding: utf-8 -*-
#   dashboard.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |---------------Fenêtre de bord--------------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from import_donnees import import_comptes, import_operations
from comptes import calcul_dict_soldes, selection_compte
from shared import saisir_choix, dict_ident


# --Constantes-- #

# --Fonctions-- #
def fenetre_bord(identifiant: int) -> int:
    """
    Donne la main à l'utilisateur pour choisir la phase suivante de l'exécution.
    0 déconnecte l'utilisateur, 1 permet d'accéder à la gestion des comptes et 2, la gestion des budgets.

    Args:
        identifiant (int): utilisé pour importer les opérations et calculer le solde du compte courant

    Returns:
        int: renvoie le choix de l'utilisateur (un entier)
    """
    cle_cryptage = dict_ident[identifiant][-1]
    lst_cpt = import_comptes(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    lst_ope = import_operations(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    dict_soldes = calcul_dict_soldes(lst_cpt, lst_ope)
    nom = dict_ident[identifiant][1]
    # selection_compte(lst_cpt) renvoie le compte courant
    solde_courant = dict_soldes[selection_compte(lst_cpt)]
    print(f"\n|-----Tableau de bord-----|\n"
          f"| Bonjour {nom} |\n"
          f"| Vous avez {solde_courant}€ sur votre compte |")

    print("\nBienvenue. De quelle fonctionnalité avez-vous besoin ?")
    print("0. Déconnexion\n"
          "1. Gestion des comptes\n"
          "2. Gestions des budgets\n")

    return saisir_choix(valeurs_autorisees={0, 1, 2})

