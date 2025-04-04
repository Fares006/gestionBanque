# gestionBanque

## Description du projet
gestionBanque est un projet universitaire de gestion de comptes bancaires et de budgets. L'application est développée en **Python** et utilise **Tkinter** pour la partie graphique (prévue en fin de projet). Ce projet académique a pour but d'offrir une interface permettant aux utilisateurs de gérer leurs comptes et budgets de manière intuitive.

## Objectif du projet
Ce projet a été réalisé dans le cadre des cours de **M. Jérôme Delobelle** et **M. Bruno Bouzy** à l'**Université Paris Cité**.

## Fonctionnalités principales
### 1. Phase d’identification
- L'utilisateur s'identifie avec un **numéro d'identifiant** (8 chiffres) et un **mot de passe** (6 chiffres).
- Un **clavier virtuel** est utilisé pour la saisie du mot de passe, avec une disposition aléatoire des chiffres.
- Les identifiants sont stockés dans un fichier sécurisé (`ident.txt`), chiffré avec le **chiffrement de César**.

### 2. Gestion des comptes
- Visualisation des comptes bancaires et de leur solde.
- Ajout d'opérations bancaires (Carte Bancaire, Chèque, Virement).
- Gestion des virements entre comptes.
- Stockage des opérations dans des fichiers utilisateurs chiffrés.

### 3. Gestion des budgets
- Création et gestion de budgets mensuels.
- Association des opérations bancaires à des budgets spécifiques.
- Affichage des dépenses par budget sous forme de **tableau**.

### 4. Autres fonctionnalités
- Calculatrice intégrée.
- Simulateur d’emprunt immobilier.

## Prérequis
- **Python 3.12**
- **Bibliothèques** : `tkinter` (pour une future interface graphique)

## Installation
1. Installer [Python 3.12](https://www.python.org/downloads/).
2. Cloner le dépôt :  
   ```sh
   git clone https://github.com/votre-utilisateur/gestionBanque.git
   cd gestionBanque
   ```

## Utilisation
### Mode Ligne de Commande (CLI)
1. Exécuter le fichier principal :
   ```sh
   python main.py
   ```

## Structure du projet
```
gestionBanque/
│
├── README.md                    # Documentation du projet
├── gestionBanque.iml            # Fichier de configuration du projet
├── misc.xml                     # Fichier de configuration supplémentaire
├── modules.xml                  # Fichier de configuration des modules
├── vcs.xml                      # Fichier de configuration du contrôle de version
├── .gitignore                   # Fichier pour ignorer des fichiers dans Git
│
├── idea/                        # Dossier de configuration IntelliJ IDEA
│   └── inspectionProfiles/
│
├── gen_users/                   # Scripts de génération des identifiants utilisateurs
│   ├── gen_ident.py             # Génère les identifiants
│   ├── gen_id_users.py          # Génère les fichiers utilisateurs
│   └── dossier_utilisateurs/    # Contient les identifiants cryptés et fichiers utilisateurs
│       ├── ident.txt            # Identifiants cryptés des utilisateurs
│       └── _users/              # Fichiers utilisateurs générés (ex : 07272359.txt, etc.)
│
├── src/                         # Code source principal
│   ├── budgets.py               # Gestion des budgets
│   ├── comptes.py               # Gestion des comptes
│   ├── cryptage_decryptage.py  # Fonctions de cryptage et décryptage
│   ├── crypter_decrypter_fichier.py # Script de cryptage/décryptage de fichiers
│   ├── dashboard.py             # Interface de tableau de bord
│   ├── gestion_budgets.py       # Contrôleur pour la gestion des budgets
│   ├── gestion_comptes.py       # Contrôleur pour la gestion des comptes
│   ├── ident.txt                # Identifiants cryptés (copie possible pour test)
│   ├── ident_clair.txt          # Identifiants en clair pour tests
│   ├── identification.py        # Module de login/identification
│   ├── import_donnees.py        # Import de données utilisateurs
│   ├── main.py                  # Point d'entrée de l'application
│   ├── main_gui.py              # Interface principale avec Tkinter
│   └── shared.py                # Fonctions partagées
│
└── users/                       # Données utilisateurs cryptées (réel ou test)
    ├── 07272359.txt
    ├── 12720138.txt
    ├── ...
    └── 96578654.txt
```

## Évolutions prévues
- Ajout progressif des fonctionnalités en mode CLI.
- Finalisation de l'interface graphique avec **Tkinter** en fin de projet.
- Amélioration de la sécurité du stockage des données.
- Ajout de la visualisation graphique des budgets.
- Documentation plus détaillée et exemples d'utilisation.
- Rapport complet et détaillé.

## Licence
Projet réalisé à des fins académiques. Toute utilisation externe doit être validée par l'Université Paris Cité.

---
📌 *Projet universitaire – Université Paris Cité*
