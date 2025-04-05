# -*- coding: utf-8 -*-
#   budgets.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |----------Phase gestion de budgets----------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from datetime import datetime
from constantes import (
    IDX_BUD_NOM,
    IDX_BUD_MONTANT,
    IDX_OPE_DATE,
    IDX_BUD_CPT,
    IDX_OPE_MONTANT,
    IDX_OPE_BUD
)
from shared import saisir_choix


# --Constantes-- #

# --Fonctions-- #
def selection_budget(lst_bud: list) -> list:
    """
    Permet à l'utilisateur de sélectionner un budget parmi ceux enregistrés.

    Affiche une liste numérotée des budgets disponibles (par leur libellé).
    L'utilisateur saisit un choix, et la fonction retourne le budget sélectionné.

    Args:
        lst_bud (list): Liste des budgets, chacun sous forme [nom, montant, compte associé].

    Returns:
        list: Le budget sélectionné (sous forme de liste).
    """
    print("Faites le choix du budget :")
    for i, bud in enumerate(lst_bud):
        print(f'{i + 1}. {bud[IDX_BUD_NOM]}')

    print("Choisissez le budget : ")
    choix = saisir_choix(valeurs_autorisees=set(range(1, len(lst_bud) + 1))) - 1
    return lst_bud[choix]


def creation_budget(lst_cpt: list, lst_bud: list) -> list:
    """
    Crée un nouveau budget à partir des saisies utilisateur, et le retourne sous forme de liste.

    La fonction demande :
    - un libellé unique (non présent dans lst_bud)
    - un montant strictement positif (float)
    - un compte associé (choisi dans lst_cpt)

    Args:
        lst_cpt (list): Liste des comptes de l'utilisateur.
        lst_bud (list): Liste des budgets existants (pour éviter les doublons de nom).

    Returns:
        list: [libellé (str), montant (float), compte associé (str)]
    """
    from comptes import selection_compte

    lst_bud_casefold = [budget[IDX_BUD_NOM].casefold() for budget in lst_bud]

    libelle = input("Libellé du nouveau budget : ").strip()
    while libelle.casefold() in lst_bud_casefold:
        print("Ce budget existe déjà.")
        libelle = input("Libellé du budget : ").strip()

    saisie_seuil_valide = False
    while not saisie_seuil_valide:
        saisie_seuil = input("Montant en € du budget (doit être supérieur à 0 €) : ")
        try:
            seuil = float(saisie_seuil)
            if seuil > 0:
                saisie_seuil_valide = True
            else:
                print("Le montant doit être strictement supérieur à 0 €.")
        except ValueError:
            print("Veuillez entrer un montant en € correct.")

    compte = selection_compte(lst_cpt, courant=False)
    return [libelle.capitalize(), seuil, compte]


def ajout_budget(lst_bud: list, budget: list) -> None:
    """
    Ajoute un budget à la liste des budgets existants de l'utilisateur,
    et affiche un message de confirmation.

    Le budget ajouté doit être une liste contenant :
        [libellé (str), montant (float), compte associé (str)]

    Args:
        lst_bud (list): Liste des budgets de l'utilisateur.
        budget (list): Le budget à ajouter (sous forme de liste).

    Returns:
        None
    """
    assert isinstance(budget, list) and len(budget) == 3, "Le budget doit être une liste de 3 éléments"
    lst_bud.append(budget)
    print(f"Le budget : {budget[IDX_BUD_NOM]} a été ajouté avec succès.")


def modifier_budget(lst_bud: list, lst_cpt: list) -> None:
    """
    Permet à l'utilisateur de modifier un budget existant parmi :
    - son libellé (nom)
    - son montant alloué
    - le compte auquel il est rattaché

    La fonction affiche un menu, puis effectue la modification choisie
    après vérification des entrées (unicité du nom, montant > 0, etc.).

    Args:
        lst_bud (list): Liste des budgets de l'utilisateur. Chaque budget est une liste :
                        [libellé (str), montant (float), compte associé (str)]
        lst_cpt (list): Liste des comptes de l'utilisateur (pour l'affectation du compte).

    Returns:
        None
    """
    from comptes import selection_compte
    
    budget_a_modifier = selection_budget(lst_bud)
    print("1. Libellé\n2. Montant\n3. Compte associé")
    choix = saisir_choix(valeurs_autorisees={1, 2, 3})

    if choix == 1:
        nouveau_libelle = input("Nouveau nom du libellé : ").strip().capitalize()
        while nouveau_libelle.casefold() == budget_a_modifier[IDX_BUD_NOM].casefold():
            nouveau_libelle = input("Le nouveau nom doit être différent.\nNouveau nom du libellé : ")
        budget_a_modifier[IDX_BUD_NOM] = nouveau_libelle
        print(f"Libellé mis à jour : {nouveau_libelle}")

    elif choix == 2:
        saisie_valide = False
        while not saisie_valide:
            saisie = input(f"Nouveau montant du budget {budget_a_modifier[IDX_BUD_NOM]} "
                           f"(actuel : {budget_a_modifier[IDX_BUD_MONTANT]:.2f} €) : ")
            try:
                nouveau_montant = float(saisie)
                if nouveau_montant > 0 and nouveau_montant != budget_a_modifier[IDX_BUD_MONTANT]:
                    saisie_valide = True
                else:
                    print("Le montant doit être supérieur à 0 et différent de l'actuel.")
            except ValueError:
                print("Veuillez entrer un montant en € valide.")
        budget_a_modifier[1] = nouveau_montant
        print(f"Montant mis à jour : {nouveau_montant:.2f} €")

    elif choix == 3:
        print(f"Compte actuel : {budget_a_modifier[IDX_BUD_CPT]}")
        nouveau_compte = selection_compte(lst_cpt, courant=False)
        budget_a_modifier[2] = nouveau_compte
        print(f"Compte associé mis à jour : {nouveau_compte}")


def rapport_bud_depenses(budget: list, lst_ope: list, date_reference: datetime.date) -> float:
    """
    Calcule le rapport entre les dépenses effectuées sur un budget donné
    et le montant alloué à ce budget pour un mois et une année spécifiés.

    Seules sont prises en compte :
    - les opérations associées au budget sélectionné,
    - dont le montant est négatif (dépense),
    - et dont la date correspond au mois et à l'année extraits de date_reference.

    Args:
        budget (list): Le budget concerné sous la forme [libellé (str), montant (float), compte (str)].
        lst_ope (list): Liste des opérations de l'utilisateur.
        date_reference (datetime.date): Date cible contenant le mois et l'année du rapport (jour ignoré).

    Returns:
        float: Le rapport entre les dépenses et le budget (ex : 0.75 pour 75%).
    """
    nom_budget = budget[IDX_BUD_NOM]
    montant_budget = budget[IDX_BUD_MONTANT]

    depenses_budget = 0.0
    for operation in lst_ope:
        if (
            operation[IDX_OPE_BUD] == nom_budget
            and operation[IDX_OPE_MONTANT] < 0
            and operation[IDX_OPE_DATE].month == date_reference.month
            and operation[IDX_OPE_DATE].year == date_reference.year
        ):
            depenses_budget += abs(operation[IDX_OPE_MONTANT])

    return depenses_budget / montant_budget if montant_budget else 0.0


# --Programme principal--
