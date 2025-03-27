#   |--------------------------------------------|   #
#   |--------Gestion de Budget (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime

# --Constantes-- #
CLE_CRYPTAGE = 23


# --Fonctions-- #
def import_idents(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> dict:
    """
    Importe le contenu du fichier ident.txt et renvoie une liste qui contient :
    l'identifiant, le mot de passe, le nom et la clé de cryptage du fichier de l'utilisateur.

    Args:
        chemin_fichier (str): le chemin relatif du fichier ident.txt
        cle (int): clé de cryptage du fichier (en dur)

    Returns:
        dict: le dictionnaire des identifiants (et informations associées dans une liste)
    """
    # Ouverture du fichier et initialisation des variables nécessaires
    dic_ident = dict()
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as idents:
        ligne = idents.readline()
        ligne = decryptage(ligne, cle=cle)
        while ligne != '':
            liste_intermediaire = ligne.strip('\n').split('*')
            dic_ident[liste_intermediaire[0]] = liste_intermediaire[1:]
            dic_ident[liste_intermediaire[0]][-1] = int(dic_ident[liste_intermediaire[0]][-1])
            ligne = idents.readline()
            ligne = decryptage(ligne, cle=cle)
    return dic_ident


def import_comptes(chemin_fichier: str, cle: int) -> list:
    """
    Importe le contenu relatif aux comptes du fichier id.txt et renvoie la liste des comptes.
    La liste contient directement les différents noms des comptes.

    Args:
        chemin_fichier (str): le chemin relatif du fichier id.txt
        cle (int): clé de cryptage du fichier

    Returns:
        list: la liste contenant les différents comptes de l'utilisateur
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
      - Une date (datetime.date) (premier élément, lst_ope[0]),
      - Un libellé de l'opération (str) (deuxième élément, lst_ope[1]),
      - Le compte concerné (str) (troisième élément, lst_ope[2]),
      - Le montant de l'opération (float) (quatrième élément, lst_ope[3]),
      - Le mode de paiement (str) (cinquième élément, lst_ope[4]),
      - Un booléen indiquant si l'opération est effective (bool) (sixième élément, lst_ope[5]),
      - Le budget concerné (str) (septième élément, lst_ope[6]).

    Args:
        chemin_fichier (str): le chemin relatif du fichier id.txt
        cle (int): clé de cryptage du fichier

    Returns:
        list: la liste des tuples contenant les différentes informations concernant chaque opération
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_ope = []
        ligne = fichier.readline()
        ligne = decryptage(ligne, cle)
        while ligne != '':
            if ligne[:3] == 'OPE':
                liste_intermediaire = ligne.strip('\n').split('*')
                liste_intermediaire.pop(0)  # On se débarrasse de 'OPE'
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
      - La catégorie de dépenses (str) (premier élément, lst_bud[0]),
      - Le montant alloué (float) (deuxième élément, lst_bud[1]),
      - Le compte associé (str) (troisième élément, lst_bud[2]).

    Args:
        chemin_fichier (str): le chemin relatif du fichier id.txt
        cle (int): clé de cryptage du fichier

    Returns:
        list: la liste des tuples contenant les différentes informations de chaque budget
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
        chaine (str): texte à crypter
        cle (int): clé qui sera utilisée pour le cryptage

    Returns:
        str: la chaine cryptée
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
        chaine (str): texte à décrypter
        cle (int): clé qui sera utilisée pour le décryptage

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
    Permet à l'utilisateur de saisir son identifiant.

    Args:

    Returns:
        str: renvoie l'identifiant de l'utilisateur validé
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
        identifiant (str): l'id de l'utilisateur validé (acquis par la fonction get_identifiant())

    Returns:
        str: renvoie le mot de passe de l'utilisateur validé
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
    Permet la connexion d'un utilisateur en utilisant le couple identifiant mot de passe.

    Args:

    Returns:
        tuple: composé de l'approbation ou non de la connexion ainsi que l'identifiant saisi.
    """
    identifiant = get_identifiant()
    if identifiant != '':
        mdp = get_mdp(identifiant)
        if mdp != '':
            return True, identifiant
    return False, identifiant


def selection_compte(lst_cpt: list, courant: bool = True) -> str:
    """
    Interface qui permet de sélectionner un compte parmis ceux qui sont présents sur
    le compte bancaire d'un utilisateur, pour diverses utilisations.

    Args:
        lst_cpt (list): contient la liste des comptes de l'utilisateur
        courant (bool): valeur True par défaut qui indique que le compte par défaut est le compte courant (compte A)

    Returns:
        str: le nom du compte
    """
    choix = 0
    if not courant:
        print("Faites le choix du compte : ")
        for i in range(len(lst_cpt)):
            print(f'{i + 1}. {lst_cpt[i]}')
        choix = int(input("Choisissez le compte: ")) - 1  # On enlève le 1 ajouté à l'affichage
        while choix not in range(len(lst_cpt)):
            choix = int(input("Choisissez le compte : ")) - 1  # On enlève le 1 ajouté à l'affichage
    compte_choisi = lst_cpt[choix]
    return compte_choisi


def selection_budget(lst_bud: list) -> str:
    """
    Interface qui permet de sélectionner un budget parmis ceux qui sont présents sur
    le compte bancaire d'un utilisateur, pour diverses utilisations.

    Args:
        lst_bud (list): contient la liste des budgets

    Returns:
        str: le nom du budget
    """
    print("Faites le choix du budget : ")
    nom_budget = [budget[0] for budget in lst_bud]
    for i in range(len(nom_budget)):
        print(f'{i + 1}. {nom_budget[i]}')
    choix = int(input("Choisissez le budget: ")) - 1  # On enlève le 1 ajouté à l'affichage
    while choix not in range(len(nom_budget)):
        choix = int(input("Choisissez le budget : ")) - 1  # On enlève le 1 ajouté à l'affichage
    budget = nom_budget[choix]
    return budget


def calcul_solde(lst_ope: list, compte: str) -> float:
    """
    Calcule le solde d'un utilisateur grâce à la liste des opérations associées au compte.

    Args:
        lst_ope: liste des opérations
        compte:

    Returns:
        le montant présent sur le compte
    """
    solde = 0
    for ope in lst_ope:
        # ope[2] représente la case contenant le compte associé à une opération donnée.
        if ope[2] == compte:
            solde += ope[3]  # ope[3] correspond au montant (+/-) de l'opération.
    return solde


def ajout_compte(lst_cpt: list, nom: str) -> None:
    """
    Ajoute un compte de type livret d'épargne, etc. à la liste des comptes de l'utilisateur prise en paramètre.

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        nom (str): le nom du nouveau compte.

    Returns:
        None
    """
    lst_cpt_minuscule = [compte.casefold() for compte in lst_cpt]
    if nom.casefold() in lst_cpt_minuscule:
        print("Le compte existe déjà.")
    else:
        lst_cpt.append(nom)
        print(f"Compte {nom} ajouté avec succès.")


def creation_operation(lst_cpt: list, lst_bud: list) -> tuple:
    """
    Crée le tuple d'une opération suite à l'entrée de l'utilisateur.

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        lst_bud (list): liste des budgets de l'utilisateur.

    Returns:
        tuple: l'opération sous forme de tuple
    """
    date_op = input("Date de l'opération (jj/mm/aaaa): ")
    while type(date_op) is not datetime.date:
        try:
            date_op = datetime.date(year=int(date_op[6:]),
                                    month=int(date_op[3:5]),
                                    day=int(date_op[:2]))
        except ValueError:
            date_op = input("Date de l'opération (jj/mm/aaaa): ")
    libelle = input("Libellé de l'opération : ")
    compte = selection_compte(lst_cpt, courant=False)
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
    budget = selection_budget(lst_bud)
    operation = date_op, libelle, compte, montant, mode_paiement, etat, budget
    return operation


def ajout_operation(lst_ope: list, operation: tuple) -> None:
    """
    Ajoute une opération (tuple) à la liste des opérations de l'utilisateur, prise en paramètre.

    Args:
        lst_ope (list): la liste des opérations à laquelle on vient ajouter la nouvelle opération.
        operation (tuple): le tuple contenant les informations relatives à une opération (date, libellé, etc.)

    Returns:
        None
    """
    lst_ope.append(operation)


def creation_budget(lst_cpt: list, lst_bud: list) -> list:
    """
    Crée la liste contenant les informations relatives à un budget, d'après l'entrée de l'utilisateur

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        lst_bud (list): liste des budgets de l'utilisateur.

    Returns:
        list: le budget sous forme de liste
    """
    lst_bud_minuscule = [budget[0].casefold() for budget in lst_bud]
    libelle = input("Libellé du nouveau budget : ")
    while libelle.casefold() in lst_bud_minuscule:
        print("Ce budget existe déjà.")
        libelle = input("Libellé du budget : ")
    seuil = float(input("Montant du budget : "))
    while seuil < 0:
        seuil = float(input("Montant du budget : "))
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
    print(f"Le budget {budget} a été ajouté avec succès.")


def creer_virement(lst_cpt: list, dict_soldes: dict) -> tuple:
    """
    Interface pour créer le virement, sous forme de tuple, afin de l'exécuter à l'aide de ajout_virement()

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        dict_soldes (dict): dictionnaire des soldes de chaque compte de l'utilisateur.

    Returns:
        tuple: le virement prêt à être exécuter.
    """
    print("Sélectionnez le compte émetteur : ")
    compte_emetteur = selection_compte(lst_cpt, courant=False)
    print("Sélectionnez le compte bénéficiaire : ")
    compte_benef = selection_compte(lst_cpt, courant=False)
    while compte_emetteur == compte_benef:
        print("Le compte émetteur doit être différent du compte bénéficiaire.")
        compte_benef = selection_compte(lst_cpt, courant=False)
    montant = float(input("Saisissez le montant du virement à effectuer : "))
    while montant > dict_soldes[compte_emetteur]:
        print(f"Il n'y a pas assez de provisions sur ce compte pour effectuer ce virement. "
              f"({montant} > {dict_soldes[compte_emetteur]})")
        montant = float(input("Saisissez le montant du virement à effectuer : "))
    virement = compte_emetteur, compte_benef, montant
    return virement


def ajout_virement(virement: tuple, lst_ope: list, dict_soldes: dict) -> None:
    """
    Effectue les modifications nécessaires aux structures pour l'exécution d'un virement d'un compte à un autre.

    Args:
        virement (tuple): tuple qui contient compte_emetteur, compte_benef, montant
        lst_ope (list): liste des opérations de l'utilisateur
        dict_soldes (dict): dictionnaire avec les soldes de chaque compte de l'utilisateur.

    Returns:
        None
    """
    ope_emetteur = (datetime.date.today(),
                    f"Virement - émetteur",
                    virement[0],    # Compte émetteur
                    -virement[2],    # Montant, négatif
                    "Application",
                    True,
                    "...")
    ope_benef = (datetime.date.today(),
                    f"Virement - bénéficiaire",
                    virement[1],    # Compte émetteur
                    virement[2],    # Montant, négatif
                    "Application",
                    True,
                    "...")
    ajout_operation(lst_ope, operation=ope_emetteur)
    ajout_operation(lst_ope, operation=ope_benef)
    dict_soldes[virement[0]] -= virement[2]
    dict_soldes[virement[1]] += virement[2]


def calcul_dict_soldes(lst_cpt, lst_ope) -> dict:
    """
    Crée un dictionnaire contenant, pour chaque compte, son solde associé

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        lst_ope (list): liste des opérations de l'utilisateur.

    Returns:
        dict: le dictionnaire {compte1 : solde1, ...}
    """
    dict_soldes = dict(zip(lst_cpt, [0 for _ in lst_cpt]))
    for ope in lst_ope:
        dict_soldes[ope[2]] = dict_soldes.get(ope[2], 0) + ope[3]
    return dict_soldes


def identification():
    """
    Fonction qui gère le comportement du logiciel, en fonction des entrées de l'utilisateur.

    Args:

    Returns:
        None
    """
    login_state = login()
    identifiant = login_state[1]
    choix = -1
    while login_state[0] and choix != 0:
        lst_cpt = import_comptes(chemin_fichier=f'../users/{identifiant}.txt', cle=dict_ident[identifiant][-1])
        lst_ope = import_operations(chemin_fichier=f'../users/{identifiant}.txt', cle=dict_ident[identifiant][-1])
        lst_bud = import_budgets(chemin_fichier=f'../users/{identifiant}.txt', cle=dict_ident[identifiant][-1])
        dict_soldes = calcul_dict_soldes(lst_cpt, lst_ope)
        # selection_compte(lst_cpt) renvoie le compte courant
        solde_courant = dict_soldes[selection_compte(lst_cpt)]
        print(f"\n|-----Tableau de bord-----|\n"
              f"| Bonjour {dict_ident[identifiant][1]} |\n"
              f"| Vous avez {solde_courant}€ sur votre compte |")

        print("\nBienvenue. De quelle fonctionnalité avez-vous besoin ?")
        print("0. Quitter le programme\n"
              "1. Afficher le solde du compte\n"
              "2. Ajouter un compte\n"
              "3. Ajouter une opération\n"
              "4. Ajouter un budget\n"
              "5. Effectuer un virement\n"
              "6. Afficher les opérations d'un compte\n"
              "7. Déconnexion\n")

        choix = int(input("Votre choix : "))

        while choix != 0:
            match choix:
                case 1:  # Solde
                    choix_compte = selection_compte(lst_cpt, courant=False)
                    solde = calcul_solde(lst_ope, choix_compte)
                    print(f"\n|-----Solde-----|\n"
                          f"| Vous avez {solde}€ sur votre compte \"{choix_compte}\" |")

                case 2:  # Ajout compte
                    print("|-----Ajout de compte-----|")
                    nouveau_compte = input("Quel est le nom du nouveau compte ? : ")
                    ajout_compte(lst_cpt, nouveau_compte)
                    solde_initial = float(input("Quel est le solde initial de ce nouveau compte ? : "))
                    dict_soldes[nouveau_compte] = solde_initial
                    ajout_operation(lst_ope, operation=(datetime.date.today(),
                                                        f"Ouverture du compte {nouveau_compte}",
                                                        nouveau_compte,
                                                        solde_initial,
                                                        True,
                                                        "..."))
                case 3:  # Ajouter une opération
                    print("|-----Ajout d'opération-----|")
                    operation = creation_operation(lst_cpt, lst_bud)
                    ajout_operation(lst_ope, operation)
                    print(f"Opération :\n{operation}\najoutée avec succès.")

                case 4:  # Ajouter un budget
                    print("|-----Ajout d'un budget-----|")
                    budget = creation_budget(lst_cpt, lst_bud)
                    ajout_budget(lst_bud, budget)
                case 5:  # Effectuer un virement entre comptes
                    print("|-----Virement compte A -> compte B-----|")
                    nouveau_virement = creer_virement(lst_cpt, dict_soldes)
                    ajout_virement(nouveau_virement, lst_ope, dict_soldes)
                case 6:  # Afficher les opérations d'un compte
                    print("|-----Affichage des opérations d'un compte-----|")
                    compte = selection_compte(lst_cpt, courant=False)
                    for operation in lst_ope:
                        print(operation, len(operation))
                        if operation[2] == compte:
                            print(f"| Date : {operation[0].strftime("%d/%m/%Y")} - "
                                  f"Libellé : {operation[1]} - "
                                  f"Montant : {operation[3]} - "
                                  f"Mode de paiement : {operation[4]} - "
                                  f"Etat : {operation[5]} - "
                                  f"Budget : {operation[6]} |")
                case 7:  # Déconnexion
                    return identification()
            choix = int(input("Quelle fonctionnalité souhaitez-vous accéder ? : "))


# --Programme principal--
if __name__ == "__main__":
    dict_ident = import_idents(chemin_fichier='./ident.txt')
    identification()
