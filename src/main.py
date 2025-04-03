# -*- coding: utf-8 -*-
#   main.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------------------------------------------|   #
# --Imports-- #
from identification import *
from dashboard import *
from gestion_comptes import gestion_comptes
from gestion_budgets import gestion_budgets


# --Constantes-- #

# --Fonctions-- #
def gestion_banque() -> None:
    """
    Fonction qui gère le comportement du logiciel, en fonction des entrées de l'utilisateur.

    Args:

    Returns:
        None
    """
    login_state = identification()
    identifiant = login_state[1]
    while login_state[0]:
        choix_phase = fenetre_bord(identifiant)
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
