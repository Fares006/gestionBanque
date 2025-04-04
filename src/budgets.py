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
    Permet à l'utilisateur de sélectionner un budget parmi ceux enregistrés.

    Affiche en console une liste numérotée des budgets disponibles (par leur libellé).
    L'utilisateur saisit un choix valide, et la fonction retourne l'entrée correspondante
    dans la liste lst_bud.

    Args:
        lst_bud (list): Liste des budgets de l'utilisateur, chaque budget étant représenté par une liste
                        [libellé (str), montant (float), compte associé (str)].

    Returns:
        list: Le budget sélectionné (sous forme de liste) parmi ceux de lst_bud.
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
    Crée un nouveau budget à partir des saisies utilisateur, et le retourne sous forme de liste.

    La fonction demande :
    - un libellé unique (non présent dans lst_bud)
    - un montant strictement positif (float)
    - un compte associé (choisi dans lst_cpt)

    Le budget est retourné sous la forme :
        [libellé (str), montant (float), compte associé (str)]

    Args:
        lst_cpt (list): Liste des comptes de l'utilisateur.
        lst_bud (list): Liste des budgets existants (pour éviter les doublons de nom).

    Returns:
        list: Le budget créé, structuré sous forme de liste.
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
    lst_bud.append(budget)
    print(f"Le budget : {budget[0]} a été ajouté avec succès.")


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
    Calcule le rapport entre les dépenses effectuées sur un budget donné
    et le montant alloué à ce budget pour un mois et une année spécifiés.

    Seules sont prises en compte :
    - les opérations associées au budget sélectionné,
    - dont le montant est négatif (dépense),
    - et dont la date correspond au mois et à l'année fournis.

    Args:
        budget (list): Le budget concerné sous la forme [libellé (str), montant (float), compte (str)].
        lst_ope (list): Liste des opérations de l'utilisateur.
        mois (int): Le mois ciblé (1 = janvier, 12 = décembre).
        annee (int): L'année ciblée (ex : 2024).

    Returns:
        float: Le rapport entre les dépenses et le budget (ex : 0.75 pour 75%).
    """
    nom_budget = budget[0]
    montant_budget = budget[1]
    depenses_budget = 0
    for operation in lst_ope:
        # operation[6] correspond au nom du budget associé à l'opération, operation[0] correspond à la date.
        if (operation[6] == nom_budget
                and operation[3] < 0     # Ne prend en compte que les opérations de dépense (montants négatifs)
                # Filtre uniquement les opérations correspondant au budget et à la période donnée
                and int(operation[0].strftime('%m')) == mois and int(operation[0].strftime('%Y')) == annee):
            depenses_budget += abs(operation[3])
    rapport = (depenses_budget / montant_budget)    # Calcule le ratio dépenses / budget
    return rapport

# --Programme principal--
