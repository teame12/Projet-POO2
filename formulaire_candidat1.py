from datetime import datetime
import sqlite3
import tkinter
from tkinter import *
from tkinter import  messagebox
from tkinter.ttk import Combobox, Treeview

from anonymat import *


class FormulaireCandidat :
    def __init__(self, parent):
        self.fenetre = tkinter.Toplevel(parent)

        self.fenetre.title("formulaire d'enregistrement des candidats")
        self.fenetre.geometry('600x600')
        self.fenetre.configure(bg="#87CEFA")

        self.conn = sqlite3.connect('base_bfem.db')
        self.cur = self.conn.cursor()

        self.num_table = None
        self.prenom = None
        self.nom = None
        self.dateNais = None
        self.lieuNais = None
        self.sexe = None
        self.nationalite = None
        self.choixEprFac = None
        self.eprFacultative = None
        self.aptSportive = None
        self.tree = None

        # Interface Graphique
        self.creer_champs()
        self.afficher_candidats()

    def creer_champs(self):
        form_frame = Frame(self.fenetre, bg="#87CEFA")
        form_frame.pack(pady=10)

        Label(form_frame, text="Numéro de table", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)
        self.num_table = Entry(form_frame, width=30)
        self.num_table.grid(row=0, column=1, padx=10, pady=10)

        Label(form_frame, text="Prénom", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=10)
        self.prenom = Entry(form_frame, width=30)
        self.prenom.grid(row=1, column=1, padx=10, pady=10)

        Label(form_frame, text="Nom", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=10, pady=10)
        self.nom = Entry(form_frame, width=30)
        self.nom.grid(row=2, column=1, padx=10, pady=10)

        Label(form_frame, text="Date de naissance (JJ/MM/AAAA)", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=10, pady=10)
        self.dateNais = Entry(form_frame, width=30)
        self.dateNais.grid(row=3, column=1, padx=10, pady=10)

        Label(form_frame, text="Lieu de naissance", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=10, pady=10)
        self.lieuNais = Entry(form_frame, width=30)
        self.lieuNais.grid(row=4, column=1, padx=10, pady=10)

        Label(form_frame, text="Sexe", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=5, column=0, padx=10, pady=10, )
        self.sexe = Combobox(form_frame, values=["Masculin", "Feminin"], width=27)
        self.sexe.grid(row=5, column=1, padx=10, pady=10)

        Label(form_frame, text="Nationalité", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=6, column=0, padx=10, pady=10)
        self.nationalite = Entry(form_frame, width=30)
        self.nationalite.grid(row=6, column=1, padx=10, pady=10)

        Label(form_frame, text="Établissement", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=1, column=2,padx=10,pady=10)
        self.etablissement = Entry(form_frame, width=30)
        self.etablissement.grid(row=1, column=3, padx=10, pady=10)

        Label(form_frame, text="Type de candidat", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=2,column=2,padx=10,pady=10)
        self.type_candidat = Combobox(form_frame, values=["Interne", "Externe"], width=27)  # Exemple de valeurs
        self.type_candidat.grid(row=2, column=3, padx=10, pady=10)

        Label(form_frame, text="Choix épreuve facultative", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=3, column=2, padx=10, pady=10)
        self.choixEprFac = Combobox(form_frame, values=["OUI", "NON"], width=27)
        self.choixEprFac.grid(row=3, column=3, padx=10, pady=10)

        Label(form_frame, text="Épreuve facultative", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=4, column=2, padx=10, pady=10)
        self.eprFacultative = Combobox(form_frame, values=["Couture", "Dessin", "Musique"], width=27)
        self.eprFacultative.grid(row=4, column=3, padx=10, pady=10)

        Label(form_frame, text="Aptitude sportive", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=5, column=2, padx=10, pady=10)
        self.aptSportive = Combobox(form_frame, values=["APTE", "INAPTE"], width=27)
        self.aptSportive.grid(row=5, column=3, padx=10, pady=10)

        # Boutons CRUD
        Button(form_frame, text="Ajouter", command=self.enregistrer_candidat,bg="#4682B4", fg="white", font=("Arial", 14, "bold")).grid(row=7, column=0, pady=10)
        Button(form_frame, text="Modifier", command=self.modifier_candidat,bg="#4682B4", fg="white", font=("Arial", 14, "bold")).grid(row=7, column=1, pady=10)
        Button(form_frame, text="Supprimer", command=self.supprimer_candidat,bg="#4682B4", fg="white", font=("Arial", 14, "bold")).grid(row=7, column=2, pady=10)

        self.tree = Treeview(self.fenetre, columns=("Numero table", "Prénom", "Nom", "Anonymat"), show="headings")
        self.tree.heading("Numero table", text="Numero table")
        self.tree.heading("Prénom", text="Prénom")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Anonymat", text="Anonymat")
        self.tree.pack(pady=10)

        # Lier la sélection dans le Treeview au formulaire
        self.tree.bind("<<TreeviewSelect>>", self.remplir_formulaire)

    def valider_donnees(self):
        # Validation du numéro de table
        if not self.num_table.get().isdigit():
            messagebox.showerror("Erreur", "Le numéro de table doit être un nombre.")
            return False

        # Validation du prénom
        if not self.prenom.get().isalpha():
            messagebox.showerror("Erreur", "Le prénom ne doit contenir que des lettres.")
            return False

        # Validation du nom
        if not self.nom.get().isalpha():
            messagebox.showerror("Erreur", "Le nom ne doit contenir que des lettres.")
            return False

        # Validation de la date de naissance
        try:
            datetime.strptime(self.dateNais.get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erreur", "La date de naissance doit être au format JJ/MM/AAAA.")
            return False

        # Validation du lieu de naissance
        if not self.lieuNais.get():
            messagebox.showerror("Erreur", "Le lieu de naissance ne doit pas être vide.")
            return False

        # Validation du sexe
        if self.sexe.get() not in ["Masculin", "Feminin"]:
            messagebox.showerror("Erreur", "Veuillez sélectionner un sexe valide.")
            return False

        # Validation de la nationalité
        if not self.nationalite.get():
            messagebox.showerror("Erreur", "La nationalité ne doit pas être vide.")
            return False

        if not self.etablissement.get():
            messagebox.showerror("Erreur", "L'établissement ne doit pas être vide.")
            return False

            # Validation du type de candidat
        if self.type_candidat.get() not in ["Interne", "Externe"]:  # Adaptez les valeurs selon vos besoins
            messagebox.showerror("Erreur", "Veuillez sélectionner un type de candidat valide.")
            return False

        # Validation du choix épreuve facultative
        if self.choixEprFac.get() not in ["OUI", "NON"]:
            messagebox.showerror("Erreur", "Veuillez sélectionner un choix valide pour l'épreuve facultative.")
            return False

        # Validation de l'épreuve facultative
        if self.choixEprFac.get() == "OUI" and not self.eprFacultative.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner une épreuve facultative.")
            return False

        # Validation de l'aptitude sportive
        if self.aptSportive.get() not in ["APTE", "INAPTE"]:
            messagebox.showerror("Erreur", "Veuillez sélectionner une aptitude sportive valide.")
            return False

        return True

    def enregistrer_candidat(self):
        if not self.valider_donnees():
            return
        try:
            self.cur.execute('''INSERT INTO Candidat (
                numero_table, prenom_s, nom, date_naissance, lieu_naissance, sexe, nationalite,
                etablissement, type_candidat, choix_epr_facultative, epreuve_facultative, aptitude_sportive
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (
                                 self.num_table.get(), self.prenom.get(), self.nom.get(), self.dateNais.get(),
                                 self.lieuNais.get(), self.sexe.get(), self.nationalite.get(), self.etablissement.get(),
                                 self.type_candidat.get(), self.choixEprFac.get(), self.eprFacultative.get(),
                                 self.aptSportive.get()
                             ))
            self.conn.commit()

            enregistrer_anonymat_principal(self.num_table.get())

            messagebox.showinfo("Succès", "Candidat enregistré avec succès.")
            self.afficher_candidats()
            self.reinitialiser_formulaire()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Ce numéro de table existe déjà.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def modifier_candidat(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]  # Prend le premier élément du tuple
            if self.valider_donnees():
                self.cur.execute('''UPDATE Candidat SET
                    prenom_s=?, nom=?, date_naissance=?, lieu_naissance=?, sexe=?, nationalite=?,
                    etablissement=?, type_candidat=?, choix_epr_facultative=?, epreuve_facultative=?, aptitude_sportive=?
                    WHERE numero_table=?''',
                                 (
                                     self.prenom.get(), self.nom.get(), self.dateNais.get(), self.lieuNais.get(),
                                     self.sexe.get(), self.nationalite.get(), self.etablissement.get(),
                                     self.type_candidat.get(),
                                     self.choixEprFac.get(), self.eprFacultative.get(), self.aptSportive.get(),
                                     self.tree.item(item_id)['values'][0]
                                 ))
                self.conn.commit()
                self.afficher_candidats()
                self.reinitialiser_formulaire()

    def supprimer_candidat(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]  # Prend le premier élément du tuple
            self.cur.execute("DELETE FROM Candidat WHERE numero_table=?", (self.tree.item(item_id)['values'][0],))
            self.conn.commit()
            self.afficher_candidats()
            self.reinitialiser_formulaire()

    def afficher_candidats(self):
        # Vider la Treeview avant d'ajouter de nouvelles données
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Récupérer les candidats depuis la base de données
        self.cur.execute('''
            SELECT Candidat.numero_table, Candidat.prenom_s, Candidat.nom, AnonymatPrincipal.anonymatPrincipal
            FROM Candidat
            LEFT JOIN AnonymatPrincipal ON Candidat.numero_table = AnonymatPrincipal.numero_table
        ''')
        rows = self.cur.fetchall()

        # Ajouter les candidats dans la Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def remplir_formulaire(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]  # Prend le premier élément du tuple
            self.reinitialiser_formulaire()

            # Récupérer le numéro de table à partir de la Treeview
            numero_table = self.tree.item(item_id)['values'][0]

            # Récupérer les informations complètes du candidat depuis la base de données
            self.cur.execute('''SELECT * FROM Candidat WHERE numero_table = ?''', (numero_table,))
            candidat = self.cur.fetchone()

            if candidat:
                # Remplir les champs du formulaire avec les données du candidat
                self.num_table.insert(0, candidat[0])  # Numéro de table
                self.prenom.insert(0, candidat[1])  # Prénom
                self.nom.insert(0, candidat[2])  # Nom
                self.dateNais.insert(0, candidat[3])  # Date de naissance
                self.lieuNais.insert(0, candidat[4])  # Lieu de naissance
                self.sexe.set(candidat[5])  # Sexe
                self.nationalite.insert(0, candidat[6])  # Nationalité
                self.etablissement.insert(0, candidat[7])  # Établissement
                self.type_candidat.set(candidat[8])  # Type de candidat

                # Vérifier si candidat[9] (choix épreuve facultative) est None ou vide
                if candidat[9] is not None:
                    self.choixEprFac.set(candidat[9])  # Choix épreuve facultative
                else:
                    self.choixEprFac.set("")  # Valeur par défaut

                # Vérifier si candidat[10] (épreuve facultative) est None ou vide
                if candidat[10] is not None:
                    self.eprFacultative.set(candidat[10])  # Épreuve facultative
                else:
                    self.eprFacultative.set("")  # Valeur par défaut

                # Vérifier si candidat[11] (aptitude sportive) est None ou vide
                if candidat[11] is not None:
                    self.aptSportive.set(candidat[11])  # Aptitude sportive
                else:
                    self.aptSportive.set("")  # Valeur par défaut

    def reinitialiser_formulaire(self):
        self.num_table.delete(0, END)
        self.prenom.delete(0, END)
        self.nom.delete(0, END)
        self.dateNais.delete(0, END)
        self.lieuNais.delete(0, END)
        self.sexe.set('')
        self.nationalite.delete(0, END)
        self.etablissement.delete(0, END)
        self.type_candidat.set('')
        self.choixEprFac.set('')
        self.eprFacultative.set('')
        self.aptSportive.set('')