# -*- coding: utf-8 -*-
#   main.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------------------------------------------|   #
# --Imports-- #
from dashboard import *
from gestion_budgets import gestion_budgets
from gestion_comptes import gestion_comptes
from identification import *


# --Constantes-- #

# --Fonctions-- #
def gestion_banque() -> None:
    """
    Gère l'exécution principale de l'application après l'authentification de l'utilisateur.

    Cette fonction :
    - Vérifie les identifiants de connexion via la fonction identification()
    - Affiche un tableau de bord avec le solde courant
    - Permet de naviguer entre deux grandes fonctionnalités :
        1. Gestion des comptes
        2. Gestion des budgets

    L'utilisateur reste dans une boucle tant qu'il ne choisit pas de se déconnecter.
    Chaque action est redirigée vers le module concerné (comptes ou budgets).

    Returns:
        None
    """
    connexion_valide, identifiant = identification()
    while connexion_valide:
        choix_phase = fenetre_bord(identifiant)
        # Boucle de navigation principale (choix utilisateur)
        match choix_phase:
            case 0:     # Déconnexion
                return gestion_banque()
            case 1:     # Gestion de comptes
                gestion_comptes(identifiant)
            case 2:     # Gestion de budgets
                gestion_budgets(identifiant)


# --Programme principal-- 
if __name__ == "__main__":
    gestion_banque()
