# -*- coding: utf-8 -*-
#   budgets.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |----------Phase gestion de budgets----------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from shared import saisir_choix


# --Constantes-- #

# --Fonctions-- #
def selection_budget(lst_bud: list) -> list:
    """
    Interface qui permet de sélectionner un budget parmi ceux qui sont présents sur
    le compte bancaire d'un utilisateur, pour diverses utilisations.

    Args:
        lst_bud (list): contient la liste des budgets

    Returns:
        list: la list qui représente le budget
    """
    nb_budgets = len(lst_bud)
    print("Faites le choix du budget : ")
    for i in range(nb_budgets):
        print(f'{i + 1}. {lst_bud[i][0]}')
    print("Choisissez le compte: ")
    choix = saisir_choix(valeurs_autorisees=set(range(1, nb_budgets + 1))) - 1  # On enlève le 1 ajouté à l'affichage
    budget = lst_bud[choix]
    return budget


def creation_budget(lst_cpt: list, lst_bud: list) -> list:
    """
    Crée la liste contenant les informations relatives à un budget, d'après l'entrée de l'utilisateur

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        lst_bud (list): liste des budgets de l'utilisateur.

    Returns:
        list: le budget sous forme de liste
    """
    from comptes import selection_compte
    lst_bud_minuscule = [budget[0].casefold() for budget in lst_bud]
    libelle = input("Libellé du nouveau budget : ")
    while libelle.casefold() in lst_bud_minuscule:
        print("Ce budget existe déjà.")
        libelle = input("Libellé du budget : ")

    saisie_seuil = input("Montant en € du budget : ")
    saisie_seuil_valide = False
    while not saisie_seuil_valide:
        try:
            seuil = float(saisie_seuil)
            if seuil > 0:
                saisie_seuil_valide = True
        except ValueError:
            print("Veuillez entrer un montant en € correct.")
            saisie_seuil = input("Montant en € du budget (doit être supérieur à 0 €) : ")

    compte = selection_compte(lst_cpt, courant=False)
    return [libelle, seuil, compte]


def ajout_budget(lst_bud: list, budget: list) -> None:
    """
    Ajoute un budget à la liste des budgets de l'utilisateur

    Args:
        lst_bud (list): la liste des budgets à laquelle nous ajoutons le nouveau budget
        budget (list): le nouveau budget

    Returns:
        None
    """
    lst_bud.append(budget)
    print(f"Le budget : {budget[0]} a été ajouté avec succès.")


def modifier_budget(lst_bud: list, lst_cpt: list) -> None:
    """
    Modifie un budget avec les informations souhaitées.

    Args:
        lst_bud (list): liste des budgets de l'utilisateur.
        lst_cpt (list): listes des comptes de l'utilisateur.

    Returns:
        None
    """
    from comptes import selection_compte
    
    budget_a_modifier = selection_budget(lst_bud)
    print("1. Libellé\n2. Montant\n3. Compte associé")
    choix = saisir_choix(valeurs_autorisees={1, 2, 3})

    if choix == 1:
        nouveau_libelle = input("Nouveau nom du libellé : ")
        while nouveau_libelle.casefold() == budget_a_modifier[0].casefold():
            nouveau_libelle = input("Le nouveau nom doit être différent.\nNouveau nom du libellé : ")
        budget_a_modifier[0] = nouveau_libelle

    elif choix == 2:
        nouveau_montant = None
        saisie_valide = False
        while not saisie_valide:
            saisie = input(f"Nouveau montant du budget {budget_a_modifier[0]} "
                           f"(actuel : {budget_a_modifier[1]:.2f} €) : ")
            try:
                nouveau_montant = float(saisie)
                if nouveau_montant != budget_a_modifier[1] and nouveau_montant > 0:
                    saisie_valide = True
                else:
                    print("Le montant doit être supérieur à 0 et différent de celui actuellement présent.")
            except ValueError:
                print("Veuillez entrer un montant en € valide.")
        budget_a_modifier[1] = nouveau_montant

    elif choix == 3:
        print(f"Compte actuel : {budget_a_modifier[2]}")
        nouveau_compte = selection_compte(lst_cpt, courant=False)
        budget_a_modifier[2] = nouveau_compte


def rapport_bud_depenses(budget: list, lst_ope: list, mois: int, annee: int) -> float:
    """
    Calcule le rapport dépense / budget pour un mois et une année donnée.

    Args:
        budget (list): liste des budgets de l'utilisateur.
        lst_ope (list): liste des opérations de l'utilisateur.
        mois (int): le mois (1-12)
        annee (int): l'année

    Returns:
        float: le rapport dépense/budget
    """
    nom_budget = budget[0]
    montant_budget = budget[1]
    depenses_budget = 0
    for operation in lst_ope:
        # operation[6] correspond au nom du budget associé à l'opération, operation[0] correspond à la date.
        if (operation[6] == nom_budget and operation[3] < 0
                and int(operation[0].strftime('%m')) == mois and int(operation[0].strftime('%Y')) == annee):
            depenses_budget += abs(operation[3])
    rapport = (depenses_budget / montant_budget)
    return rapport

# --Programme principal--
