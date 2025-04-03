# main_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from random import shuffle
import datetime
from main import *


class ClavierVirtuel(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.mdp = ""
        self.build_keyboard()

    def build_keyboard(self):
        self.title("Clavier virtuel")
        self.geometry("250x250")

        digits = [str(i) for i in range(10)]
        shuffle(digits)
        buttons = digits + ["Annuler", "Valider"]

        for i, val in enumerate(buttons):
            cmd = lambda v=val: self.on_button_click(v)
            tk.Button(self, text=val, width=6, height=2, command=cmd).grid(row=i // 3, column=i % 3)

    def on_button_click(self, value):
        if value == "Annuler":
            self.mdp = ""
        elif value == "Valider":
            self.callback(self.mdp)
            self.destroy()
        else:
            self.mdp += value


class FenetreConnexion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion")
        self.geometry("300x200")
        self.identifiants = import_idents("ident.txt", cle=CLE_CRYPTAGE)
        self.mdp = ""
        self.build()

    def build(self):
        tk.Label(self, text="Identifiant (8 chiffres)").pack()
        self.entry_id = tk.Entry(self)
        self.entry_id.pack(pady=5)
        tk.Button(self, text="Saisir mot de passe", command=self.ouvrir_clavier).pack(pady=5)
        self.label_info = tk.Label(self, text="")
        self.label_info.pack()
        tk.Button(self, text="Connexion", command=self.connexion).pack(pady=10)

    def ouvrir_clavier(self):
        ClavierVirtuel(self, self.recuperer_mdp)

    def recuperer_mdp(self, mdp):
        self.mdp = mdp
        self.label_info.config(text=f"Mot de passe saisi ({len(mdp)} chiffres)")

    def connexion(self):
        id_ = self.entry_id.get()
        if id_ in self.identifiants and self.mdp == self.identifiants[id_][0]:
            nom = self.identifiants[id_][1]
            cle = self.identifiants[id_][2]
            self.destroy()
            FenetreBord(id_, nom, cle).mainloop()
        else:
            messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect.")


class FenetreBord(tk.Tk):
    def __init__(self, identifiant, nom, cle):
        super().__init__()
        self.identifiant, self.nom, self.cle = identifiant, nom, cle
        self.lst_cpt = import_comptes(f"../users/{identifiant}.txt", cle)
        self.lst_ope = import_operations(f"../users/{identifiant}.txt", cle)
        self.lst_bud = import_budgets(f"../users/{identifiant}.txt", cle)
        self.dict_soldes = calcul_dict_soldes(self.lst_cpt, self.lst_ope)
        self.compte_selectionne = self.lst_cpt[0]
        self.build()

    def build(self):
        self.title("Tableau de bord")
        self.geometry("400x600")

        tk.Label(self, text=f"Bienvenue {self.nom}", font=("Arial", 14)).pack(pady=10)
        self.solde_label = tk.Label(self, text=f"Solde: {self.dict_soldes[self.compte_selectionne]:.2f}€")
        self.solde_label.pack(pady=5)

        self.combo = ttk.Combobox(self, values=self.lst_cpt, state="readonly")
        self.combo.current(0)
        self.combo.pack(pady=5)
        self.combo.bind("<<ComboboxSelected>>", self.update_compte)

        tk.Button(self, text="Ajouter un compte", command=self.ajouter_compte).pack(pady=2)
        tk.Button(self, text="Ajouter une opération", command=self.ajouter_operation).pack(pady=2)
        tk.Button(self, text="Effectuer un virement", command=self.effectuer_virement).pack(pady=2)
        tk.Button(self, text="Ajouter un budget", command=self.ajouter_budget).pack(pady=2)
        tk.Button(self, text="Modifier un budget", command=self.modifier_budget).pack(pady=2)
        tk.Button(self, text="Afficher opérations", command=self.afficher_operations).pack(pady=2)
        tk.Button(self, text="Rapport budget", command=self.rapport_budget).pack(pady=2)
        tk.Button(self, text="Déconnexion", command=self.logout).pack(pady=10)

    def update_compte(self, event):
        self.compte_selectionne = self.combo.get()
        self.solde_label.config(text=f"Solde: {self.dict_soldes[self.compte_selectionne]:.2f}€")

    def ajouter_compte(self):
        nom = simpledialog.askstring("Compte", "Nom du compte:")
        if nom:
            ajout_compte(self.lst_cpt, nom)
            montant = float(simpledialog.askstring("Montant", "Solde initial:"))
            self.dict_soldes[nom] = montant
            self.lst_ope.append((datetime.date.today(), f"Ouverture {nom}", nom, montant, "Application", True, "..."))
            messagebox.showinfo("Succès", f"Compte {nom} ajouté.")
            self.combo['values'] = self.lst_cpt

    def ajouter_operation(self):
        operation = creation_operation(self.lst_cpt, self.lst_bud)
        ajout_operation(self.lst_ope, operation)
        messagebox.showinfo("Ajouté", f"Opération ajoutée: {operation[1]}")

    def effectuer_virement(self):
        virement = creer_virement(self.lst_cpt, self.dict_soldes)
        ajout_virement(virement, self.lst_ope, self.dict_soldes)
        messagebox.showinfo("Succès", "Virement effectué.")

    def ajouter_budget(self):
        budget = creation_budget(self.lst_cpt, self.lst_bud)
        ajout_budget(self.lst_bud, budget)
        messagebox.showinfo("Succès", "Budget ajouté.")

    def modifier_budget(self):
        modifier_budget(self.lst_bud, self.lst_cpt)

    def afficher_operations(self):
        ops = [f"{ope[0]} - {ope[1]} - {ope[3]}€" for ope in self.lst_ope if ope[2] == self.compte_selectionne]
        messagebox.showinfo("Opérations", "\n".join(ops))

    def rapport_budget(self):
        mois = simpledialog.askinteger("Mois", "Numéro du mois (1-12):")
        annee = simpledialog.askinteger("Année", "Année:")
        budget = selection_budget(self.lst_bud)
        rapport = rapport_bud_depenses(budget, self.lst_ope, mois, annee)
        messagebox.showinfo("Rapport", f"{rapport*100:.1f}% du budget utilisé")

    def logout(self):
        enregistrement_modif(self.lst_cpt, self.lst_ope, self.lst_bud, self.identifiant, self.cle)
        self.destroy()
        FenetreConnexion().mainloop()


if __name__ == '__main__':
    FenetreConnexion().mainloop()
