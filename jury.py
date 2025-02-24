import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox

class FormulaireJury:
    def __init__(self, parent):
        self.fenetre = tkinter.Toplevel(parent)

        self.fenetre.title("Paramétrage du jury")
        self.fenetre.geometry("600x600")
        self.fenetre.configure(bg="#87CEFA")

        # Région
        Label(self.fenetre, text="Région", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.region = Entry(self.fenetre, width=30)
        self.region.grid(row=0, column=1, padx=10, pady=10)

        # Département
        Label(self.fenetre, text="Département", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.departement = Entry(self.fenetre, width=30)
        self.departement.grid(row=1, column=1, padx=10, pady=10)

        # Localité
        Label(self.fenetre, text="Localité", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.localite = Entry(self.fenetre, width=30)
        self.localite.grid(row=2, column=1, padx=10, pady=10)

        # Centre d'examen
        Label(self.fenetre, text="Centre d'examen", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.ctrExamen = Entry(self.fenetre, width=30)
        self.ctrExamen.grid(row=3, column=1, padx=10, pady=10)

        # Président Jury
        Label(self.fenetre, text="Président Jury", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.preJury = Entry(self.fenetre, width=30)
        self.preJury.grid(row=4, column=1, padx=10, pady=10)

        # Téléphone
        Label(self.fenetre, text="Téléphone", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.telephone = Entry(self.fenetre, width=30)
        self.telephone.grid(row=5, column=1, padx=10, pady=10)

        Button(self.fenetre, text="Enregistrer", command=self.enregistrer_jury, bg="#4682B4", fg="white", font=("Arial", 14, "bold")).grid(row=6, column=1, columnspan=2, pady=10)

    def valider_donnees(self):
        # Vérifier que tous les champs obligatoires sont remplis
        if not self.region.get() or not self.departement.get() or not self.localite.get() or not self.ctrExamen.get() or not self.preJury.get() or not self.telephone.get():
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return False

        # Vérifier que le téléphone est un nombre
        if not self.telephone.get().isdigit():
            messagebox.showerror("Erreur", "Le téléphone doit être un nombre.")
            return False

        return True

    def enregistrer_jury(self):
        if not self.valider_donnees():
            return

        conn = sqlite3.connect("base_bfem.db")
        try:
            cur = conn.cursor()
            cur.execute('''INSERT INTO Jury (region, departement, localite, centre_examen, president_jury, telephone)
                                   VALUES (?, ?, ?, ?, ?, ?)''',
                        (self.region.get(), self.departement.get(), self.localite.get(), self.ctrExamen.get(),
                         self.preJury.get(), self.telephone.get()))

            conn.commit()
            messagebox.showinfo("Succès", "Informations du jury enregistrées avec succès.")
            self.reinitialiser_formulaire()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur",
                                 "Une erreur s'est produite lors de l'enregistrement (violation de contrainte).")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
        finally:
            conn.close()

    def reinitialiser_formulaire(self):
        # Réinitialiser tous les champs
        self.region.delete(0, END)
        self.departement.delete(0, END)
        self.localite.delete(0, END)
        self.ctrExamen.delete(0, END)
        self.preJury.delete(0, END)
        self.telephone.delete(0, END)