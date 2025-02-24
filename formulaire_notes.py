import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class FormulaireNotes:
    def __init__(self, parent):
        self.fenetre = tkinter.Toplevel(parent)
        self.fenetre.title('Formulaire de saisie de notes')
        self.fenetre.geometry("1000x600")  # Taille initiale de la fenêtre
        self.fenetre.configure(bg="#87CEFA")

        # Configuration des poids des colonnes et des lignes
        self.fenetre.columnconfigure(0, weight=1)
        self.fenetre.columnconfigure(1, weight=1)
        self.fenetre.rowconfigure(1, weight=1)  # Ligne pour les champs de saisie
        self.fenetre.rowconfigure(2, weight=3)  # Ligne pour la Treeview

        # Frame pour les champs de saisie
        frame_saisie = Frame(self.fenetre, bg="#87CEFA")
        frame_saisie.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Champ pour le numéro d'anonymat
        Label(frame_saisie, text="Numéro d'Anonymat:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.anonymat = Entry(frame_saisie)
        self.anonymat.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Champs pour les notes
        Label(frame_saisie, text="Composition Française:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.compo_franc = Entry(frame_saisie)
        self.compo_franc.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="Dictée:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.dictee = Entry(frame_saisie)
        self.dictee.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="Étude de Texte:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.etude_texte = Entry(frame_saisie)
        self.etude_texte.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="Instruction Civique:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.instruction_civique = Entry(frame_saisie)
        self.instruction_civique.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="Histoire Géographie:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.histoire_geo = Entry(frame_saisie)
        self.histoire_geo.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="Mathématiques:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.mathematiques = Entry(frame_saisie)
        self.mathematiques.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="PC/LV2:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.pc_lv2 = Entry(frame_saisie)
        self.pc_lv2.grid(row=1, column=3, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="SVT:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=2, column=2, padx=5, pady=5, sticky='w')
        self.svt = Entry(frame_saisie)
        self.svt.grid(row=2, column=3, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="Anglais Ecrit:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=3, column=2, padx=5, pady=5, sticky='w')
        self.anglais_ecrit = Entry(frame_saisie)
        self.anglais_ecrit.grid(row=3, column=3, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="Anglais Oral:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=4, column=2, padx=5, pady=5, sticky='w')
        self.anglais_oral = Entry(frame_saisie)
        self.anglais_oral.grid(row=4, column=3, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="EPS:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=5, column=2, padx=5, pady=5, sticky='w')
        self.eps = Entry(frame_saisie)
        self.eps.grid(row=5, column=3, padx=5, pady=5, sticky='ew')

        Label(frame_saisie, text="Épreuve Facultative:", bg="#87CEFA", fg="white", font=("Arial", 14, "bold")).grid(row=6, column=2, padx=5, pady=5, sticky='w')
        self.epreuve_facultative = Entry(frame_saisie)
        self.epreuve_facultative.grid(row=6, column=3, padx=5, pady=5, sticky='ew')

        # Boutons
        Button(frame_saisie, text="Enregistrer", command=self.enregistrer_notes, bg="#4682B4", fg="white", font=("Arial", 14, "bold")).grid(row=7, column=0, columnspan=2, pady=10)
        Button(frame_saisie, text="Afficher les notes", command=self.afficher_notes, bg="#4682B4", fg="white", font=("Arial", 14, "bold")).grid(row=7, column=2, columnspan=2, pady=10)

        # Treeview avec barres de défilement
        frame_treeview = Frame(self.fenetre)
        frame_treeview.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Barre de défilement verticale
        scrollbar_y = ttk.Scrollbar(frame_treeview, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        # Barre de défilement horizontale
        scrollbar_x = ttk.Scrollbar(frame_treeview, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        # Configuration de la Treeview
        self.tree = ttk.Treeview(
            frame_treeview,
            columns=("Épreuve", "Note"),  # Deux colonnes : Épreuve et Note
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        self.tree.pack(side="left", fill="both", expand=True)

        # Configuration des barres de défilement
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # En-têtes de la Treeview
        self.tree.heading("Épreuve", text="Épreuve")
        self.tree.heading("Note", text="Note")

        # Ajuster la largeur des colonnes
        self.tree.column("Épreuve", width=200, anchor="center")
        self.tree.column("Note", width=100, anchor="center")

    def valider_notes(self, note):
        """Valide que la note est comprise entre 0 et 20."""
        if note.strip() == "":  # Si la note est vide
            return True  # Permettre les notes vides (optionnel)
        try:
            note = float(note)
            return 0 <= note <= 20
        except ValueError:
            return False

    def enregistrer_notes(self):
        notes = [
            self.compo_franc.get(),
            self.dictee.get(),
            self.etude_texte.get(),
            self.instruction_civique.get(),
            self.histoire_geo.get(),
            self.mathematiques.get(),
            self.pc_lv2.get(),
            self.svt.get(),
            self.anglais_ecrit.get(),
            self.anglais_oral.get(),
            self.eps.get(),
            self.epreuve_facultative.get()
        ]

        # Valider les notes
        for note in notes:
            if not self.valider_notes(note):
                messagebox.showerror("Erreur", "Les notes doivent être comprises entre 0 et 20")
                return

        try:
            conn = sqlite3.connect('base_bfem.db')
            cur = conn.cursor()

            # Vérifier si le numéro d'anonymat existe dans AnonymatPrincipal
            cur.execute('''SELECT numero_table FROM AnonymatPrincipal WHERE anonymatPrincipal = ?''',
                        (self.anonymat.get(),))
            result = cur.fetchone()

            if not result:
                messagebox.showerror("Erreur", "Numéro d'anonymat invalide")
                return

            numero_table = result[0]

            # Insérer les notes
            cur.execute('''
                INSERT INTO Notes (numero_table, compo_franc, dictee, etude_de_texte, instruction_Civique, histoire_Geographie, mathematiques, pc_lv2, SVT, anglais1, anglais_oral, eps, epreuve_facultative)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                numero_table,
                self.compo_franc.get() or None,  # Remplace une chaîne vide par NULL
                self.dictee.get() or None,
                self.etude_texte.get() or None,
                self.instruction_civique.get() or None,
                self.histoire_geo.get() or None,
                self.mathematiques.get() or None,
                self.pc_lv2.get() or None,
                self.svt.get() or None,
                self.anglais_ecrit.get() or None,
                self.anglais_oral.get() or None,
                self.eps.get() or None,
                self.epreuve_facultative.get() or None
            ))
            conn.commit()
            messagebox.showinfo("Succès", "Notes enregistrées avec succès !")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'enregistrement : {e}")
        finally:
            conn.close()

    def afficher_notes(self):
        anonymat = self.anonymat.get()
        if not anonymat:
            messagebox.showerror("Erreur", "Veuillez entrer le numéro d'anonymat")
            return

        try:
            conn = sqlite3.connect("base_bfem.db")
            cur = conn.cursor()

            # Récupérer le numéro de table associé à l'anonymat principal
            cur.execute('''SELECT numero_table FROM AnonymatPrincipal WHERE anonymatPrincipal = ?''', (anonymat,))
            result = cur.fetchone()

            if not result:
                messagebox.showerror("Erreur", "Numéro d'anonymat invalide")
                return

            numero_table = result[0]

            # Récupérer les notes associées au numéro de table
            cur.execute('''
                SELECT compo_franc, dictee, etude_de_texte, instruction_Civique, histoire_Geographie, mathematiques, pc_lv2, SVT, anglais1, anglais_oral, eps, epreuve_facultative
                FROM Notes 
                WHERE numero_table = ?
            ''', (numero_table,))
            notes = cur.fetchone()
            conn.close()

            if notes:
                # Liste des épreuves
                epreuves = [
                    "Composition Française", "Dictée", "Étude de texte", "Instruction Civique",
                    "Histoire-Géographie", "Mathématiques", "PC/LV2", "SVT", "Anglais écrit",
                    "Anglais oral", "EPS", "Épreuve facultative"
                ]

                # Vider la Treeview avant d'ajouter de nouvelles données
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Ajouter les épreuves et les notes dans la Treeview
                for epreuve, note in zip(epreuves, notes):
                    if note is not None:  # Ignorer les notes nulles
                        self.tree.insert("", "end", values=(epreuve, note))
            else:
                messagebox.showinfo("Aucune note trouvée", "Aucune note trouvée pour ce numéro d'anonymat.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")