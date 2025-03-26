#   |--------------------------------------------|   #
#   |--------Gestion de Budget (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime
import tkinter as tk
from pprint import pprint
from tkinter import messagebox

# --Constantes-- #
CLE_CRYPTAGE = 23


# --Fonctions-- #
def import_idents(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> dict:
    """
    Importe le contenu du fichier ident.txt et renvoie une liste qui contient :
    l'identifiant, le mot de passe, le nom et la clé de cryptage du fichier de l'utilisateur.

    Args:
        chemin_fichier: le chemin relatif du fichier ident.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        le dictionnaire des identifiants (et informations associées dans une liste)
    """
    # Ouverture du fichier et initialisation des variables nécessaires
    dic_ident = dict()
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as idents:
        ligne = idents.readline()
        ligne = decryptage(ligne, cle=cle)
        while ligne != '':
            liste_intermediaire = ligne.split('*')
            dic_ident[liste_intermediaire[0]] = liste_intermediaire[1:]
            dic_ident[liste_intermediaire[0]][-1] = int(dic_ident[liste_intermediaire[0]][-1])
            ligne = idents.readline()
            ligne = decryptage(ligne, cle=cle)
    return dic_ident


def import_comptes(chemin_fichier: str, cle: int) -> list:
    """
    Importe le contenu relatif aux comptes du fichier id.txt et renvoie la liste des comptes.

    Args:
        chemin_fichier: le chemin relatif du fichier id.txt
        cle: clé de cryptage du fichier

    Returns:
        la liste contenant les différents comptes de l'utilisateur
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_comptes = []
        ligne = fichier.readline()
        ligne = decryptage(ligne, cle)
        while ligne != '' and ligne[:3] == 'CPT':
            liste_intermediaire = ligne.strip('\n').split('*')
            liste_comptes.append(liste_intermediaire[1])
            ligne = fichier.readline()
            ligne = decryptage(ligne, cle)
    return liste_comptes


def import_operations(chemin_fichier: str, cle: int) -> list:
    """
    Importe le contenu relatif aux opérations du fichier id.txt et renvoie une liste de tuples qui contient :
      - Une date (datetime.date),
      - Un libellé de l'opération (str),
      - Le compte concerné (str),
      - Le montant de l'opération (float),
      - Le mode de paiement (str),
      - Un booléen indiquant si l'opération est effective (bool),
      - Le budget concerné (str).

    Args:
        chemin_fichier: le chemin relatif du fichier id.txt
        cle: clé de cryptage du fichier

    Returns:
        la liste des tuples contenant les différentes informations concernant chaque opération
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_ope = []
        ligne = fichier.readline()
        ligne = decryptage(ligne, cle)
        while ligne != '':
            if ligne[:3] == 'OPE':
                liste_intermediaire = ligne.strip('\n').split('*')
                liste_intermediaire.pop(0)
                liste_intermediaire[0] = datetime.date(year=int(liste_intermediaire[0][6:]),
                                                       month=int(liste_intermediaire[0][3:5]),
                                                       day=int(liste_intermediaire[0][0:2]))
                liste_intermediaire[3] = float(liste_intermediaire[3])
                liste_intermediaire[5] = bool(liste_intermediaire[5])
                liste_ope.append(tuple(liste_intermediaire))
            ligne = fichier.readline()
            ligne = decryptage(ligne, cle)
    return liste_ope


def import_budgets(chemin_fichier: str, cle: int) -> list:
    """
    Importe le contenu relatif aux budgets du fichier id.txt et renvoie une liste de listes qui contient :
      - La catégorie de dépenses (str),
      - Le montant alloué (float),
      - Le compte associé (str).

    Args:
        chemin_fichier: le chemin relatif du fichier id.txt
        cle: clé de cryptage du fichier

    Returns:
        la liste des tuples contenant les différentes informations de chaque budget
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_bud = []
        ligne = fichier.readline()
        ligne = decryptage(ligne, cle)
        while ligne != '':
            if ligne[:3] == 'BUD':
                liste_intermediaire = ligne.strip('\n').split('*')
                liste_intermediaire.pop(0)
                liste_intermediaire[1] = float(liste_intermediaire[1])
                liste_bud.append(liste_intermediaire)
            ligne = fichier.readline()
            ligne = decryptage(ligne, cle)
    return liste_bud


def cryptage(chaine: str, cle: int) -> str:
    """
    Fonction, avec 2 options en paramètres, qui renvoie une chaîne de caractères cryptée
    avec la méthode César, selon la clé fournie.

    Args:
        chaine: texte à crypter
        cle: clé qui sera utilisée pour le cryptage

    Returns:
        la chaine cryptée
    """
    crypte = ''
    for char in chaine:
        if char == '\n' or char == '*':
            crypte += char
        else:
            crypte += chr(ord(char) + cle)
    return crypte


def decryptage(chaine: str, cle: int) -> str:
    """
    Fonction, avec 2 options en paramètres, qui renvoie une chaîne de caractères décryptée
    avec la méthode César, selon la clé fournie.

    Args:
        chaine: texte à décrypter
        cle: clé qui sera utilisée pour le décryptage

    Returns:
        str: la chaine décryptée
    """
    decrypte = ''
    for char in chaine:
        if char == '\n' or char == '*':
            decrypte += char
        else:
            decrypte += chr(ord(char) - cle)
    return decrypte


def get_identifiant() -> str:
    """
    Permet à l'utilisateur de saisir son identifiant

    Returns:
        renvoie l'identifiant de l'utilisateur validé
    """
    identifiant_trouve = False
    nb_essais = 0
    while nb_essais < 5 and not identifiant_trouve:
        identifiant = input('Veuillez saisir votre identifiant : ')
        if len(identifiant) != 8:
            print('L\'identifiant doit faire 8 caractères.')
        elif identifiant not in dict_ident.keys():
            nb_essais += 1
            print(f"Identifiant introuvable. Vous avez {5 - nb_essais} essais restants.")
        else:
            identifiant_trouve = True
            return identifiant
    return ''


def get_mdp(identifiant: str) -> str:
    """
    Permet à l'utilisateur de saisir son mot de passe.

    Args:
        identifiant: l'id de l'utilisateur validé (acquis par la fonction get_identifiant())

    Returns:
        renvoie le mot de passe de l'utilisateur validé
    """
    connecte = False
    nb_essais = 0
    while nb_essais < 5 and not connecte:
        mdp = input('Veuillez saisir votre mot de passe : ')
        if len(mdp) != 6:
            print('Le mot de passe doit faire 6 caractères.')
        elif mdp != dict_ident[identifiant][0]:
            nb_essais += 1
            print(f"Mot de passe incorrect. Vous avez {5 - nb_essais} essais restants.")
        else:
            connecte = True
            return mdp
    return ''


def login() -> tuple:
    """

    Args:

    Returns:
    """
    identifiant = get_identifiant()
    if identifiant != '':
        mdp = get_mdp(identifiant)
        if mdp != '':
            return True, identifiant
    return False, identifiant


def calcul_solde(lst_cpt: list, lst_ope: list, courant=False) -> float:
    """
    Calcule le solde d'un utilisateur grâce à la liste des opérations associées au compte.

    Args:
        lst_ope: liste des opérations

    Returns:
        le montant présent sur le compte
    """
    choix = 0
    if not courant:
        print("Faites le choix du compte : ")
        for i in range(len(lst_cpt)):
            print(f'{i + 1}. {lst_cpt[i]}')
        choix = int(input("Choisissez le compte pour calculer son solde : ")) - 1  # On enlève le 1 de l'affichage
        while choix not in list(range(len(lst_cpt))):
            choix = int(input("Choisissez le compte pour calculer son solde : ")) - 1  # On enlève le 1 de l'affichage

    compte_choisi = lst_cpt[choix]
    solde = 0
    for i in range(len(lst_ope)):
        if lst_ope[i][2] == compte_choisi:
            solde += lst_ope[i][3]
    return solde


def ajout_compte(lst_cpt: list) -> None:
    """
    Ajoute un compte de type livret d'épargne, etc. à la liste des comptes de l'utilisateur prise en paramètre.

    Args:
        lst_cpt: liste des comptes de l'utilisateur.

    Returns:
        None
    """
    nom = input("Nom du nouveau compte désiré : ")
    lst_cpt.append(nom)


def ajout_operation(lst_ope: list, lst_cpt: list, lst_bud: list) -> None:
    """
    Ajoute une opération (tuple) à la liste des opérations de l'utilisateur, prise en paramètre.

    Args:
        lst_ope: liste des opérations associées au compte.

    Returns:
        None
    """
    date_op = input("Date de l'opération (jj/mm/aaaa): ")
    while type(date_op) is not datetime.date:
        try:
            date_op = datetime.date(year=int(date_op[6:]),
                                    month=int(date_op[3:5]),
                                    day=int(date_op[0:2]))
        except TypeError:
            date_op = input("Date de l'opération (jj/mm/aaaa): ")
    libelle = input("Libellé : ")
    compte = input("Compte concerné : ")
    while compte not in lst_cpt:
        print("Compte introuvable.")
        compte = input("Compte concerné : ")
    montant = float(input("Montant (positif / négatif) : "))
    mode_paiement = input("Mode de paiement : ")
    etat = input("L'opération est elle passée ? (O/N) : ").capitalize()
    while etat not in ['O', 'N']:
        etat = input("L'opération est elle passée ? (O/N) : ").capitalize()
    match etat:
        case 'O':
            etat = True
        case 'N':
            etat = False
    budget = input("Budget : ")
    nom_budget = [lst_bud[i][0] for i in range(len(lst_bud))]
    while budget not in nom_budget:
        budget = input("Budget : ")
    operation = date_op, libelle, compte, montant, mode_paiement, etat, budget
    lst_ope.append(operation)


def identification():
    """
    Fonction qui gère le comportement du logiciel, en fonction des entrées de l'utilisateur.

    Returns:

    """
    login_state = login()
    identifiant = login_state[1]
    if login_state[0]:
        lst_cpt = import_comptes(chemin_fichier=f'../users/{identifiant}.txt', cle=dict_ident[identifiant][-1])
        lst_ope = import_operations(chemin_fichier=f'../users/{identifiant}.txt', cle=dict_ident[identifiant][-1])
        lst_bud = import_budgets(chemin_fichier=f'../users/{identifiant}.txt', cle=dict_ident[identifiant][-1])

        solde_courant = calcul_solde(lst_cpt, lst_ope, courant=True)
        print(f"\n|-----Tableau de bord-----|\n"
              f"| Bonjour {dict_ident[identifiant][1]} |\n"
              f"| Vous avez {solde_courant}€ sur votre compte |")

        print("\nBienvenue. De quelle fonctionnalité avez-vous besoin ?")
        print("0. Quitter\n"
              "1. Afficher le solde du compte\n"
              "2. Ajouter un compte\n"
              "3. Ajouter une opération\n"
              "4. Effectuer un virement\n"
              "5. Afficher les opérations d'un compte\n")
        choix = int(input("Votre choix : "))
        while choix != 0:
            match choix:
                case 1:
                    solde = calcul_solde(lst_cpt, lst_ope)
                    print(f"\n|-----Solde-----|\n"
                          f"| Vous avez {solde}€ sur votre compte 635"
                          f"1*£|")
                    choix = int(input("Quelle fonctionnalité souhaitez-vous accéder ? : "))
                case 2:
                    print("|-----Ajout de compte-----|")
                    ajout_compte()
                    print(f"Compte {lst_cpt[-1]} ajouté avec succès.")
                    choix = int(input("Quelle fonctionnalité souhaitez-vous accéder ? : "))
                case 3:
                    print("|-----Ajout d'opération-----|")
                    ajout_operation()
                    print(f"Opération : \n{lst_ope[-1]}\n ajoutée avec succès.")
                    choix = int(input("Quelle fonctionnalité souhaitez-vous accéder ? : "))
                case 4:
                    pass
                case 5:
                    for elt in lst_ope:
                        print(elt)
                    choix = int(input("Quelle fonctionnalité souhaitez-vous accéder ? : "))


# --Programme principal--
if __name__ == "__main__":
    dict_ident = import_idents(chemin_fichier='./ident.txt')
    identification()
