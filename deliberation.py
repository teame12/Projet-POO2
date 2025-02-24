import sqlite3
import tkinter
from tkinter import ttk

class FormulaireDeliberation:
    def __init__(self, parent):
        self.fenetre = tkinter.Toplevel(parent)
        self.fenetre.title("Délibération")
        self.fenetre.geometry("1100x600")
        self.fenetre.configure(bg="#87CEFA")

        # Connexion à la base de données
        self.conn = sqlite3.connect('base_bfem.db')
        self.cur = self.conn.cursor()

        # Treeview pour afficher les résultats
        self.tree = ttk.Treeview(self.fenetre, columns=("Numéro", "Nom", "Prénom", "Points", "Résultat"), show="headings")
        self.tree.heading("Numéro", text="Numéro")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Prénom", text="Prénom")
        self.tree.heading("Points", text="Points")
        self.tree.heading("Résultat", text="Résultat")
        self.tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Bouton pour calculer les résultats
        tkinter.Button(self.fenetre, text="Calculer les résultats",bg="#4682B4", fg="white", font=("Arial", 14, "bold"), command=self.calculer_resultats).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def calculer_resultats(self):
        """Calcule les points et détermine le résultat pour chaque candidat."""
        # Vider la Treeview avant d'insérer de nouveaux résultats
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Récupérer les candidats et leurs notes
        self.cur.execute('''
            SELECT Candidat.numero_table, Candidat.Nom, Candidat.Prenom_s, 
                   Notes.compo_franc, Notes.dictee, Notes.etude_de_texte, Notes.instruction_Civique, 
                   Notes.histoire_Geographie, Notes.mathematiques, Notes.pc_lv2, Notes.SVT, Notes.anglais1, 
                   Notes.anglais_oral, Notes.eps, Notes.epreuve_facultative,
                   Livret_Scolaire.moyenne_Cycle, Livret_Scolaire.nombre_de_fois, Candidat.aptitude_sportive
            FROM Candidat
            JOIN Notes ON Candidat.numero_table = Notes.numero_table
            JOIN Livret_Scolaire ON Candidat.numero_table = Livret_Scolaire.numero_table
        ''')
        candidats = self.cur.fetchall()

        for candidat in candidats:
            # Remplacement des valeurs None par 0
            notes = [(note if note is not None else 0) for note in candidat[3:15]]

            # Vérifier si le candidat est apte pour l'EPS
            aptitude_sportive = candidat[17]  # aptitude_sportive

            # Validation des notes
            try:
                self.valider_notes(notes)
            except ValueError as e:
                print(f"Erreur de validation des notes pour le candidat {candidat[0]} : {e}")
                continue  # Ignorer ce candidat et passer au suivant

            # Calculer les points totaux
            points = (
                    notes[0] * 2 +  # Compo Française
                    notes[1] * 1 +  # Dictée
                    notes[2] * 1 +  # Étude de texte
                    notes[3] * 1 +  # Instruction Civique
                    notes[4] * 2 +  # Histoire-Géographie
                    notes[5] * 4 +  # Mathématiques
                    notes[6] * 2 +  # PC/LV2
                    notes[7] * 2 +  # SVT
                    notes[8] * 2 +  # Anglais 1
                    notes[9] * 1   # Anglais oral
            )

            # Appliquer les bonus/malus pour l'EPS (seulement si le candidat est apte)
            if aptitude_sportive == 1:
                if notes[10] > 10:  # Bonus EPS
                    points += (notes[10] - 10)
                elif notes[10] < 10:  # Malus EPS
                    points -= (10 - notes[10])

            # Appliquer le bonus pour l'épreuve facultative
            if notes[11] > 10:
                points += (notes[11] - 10)

            # Déterminer le résultat en appliquant RM7, RM8 et RM9
            moyenne_cycle = candidat[15] if candidat[15] is not None else 0  # moyenne_Cycle
            nombre_tentatives = candidat[16] if candidat[16] is not None else 0  # nombre_de_fois

            if points >= 180:
                resultat = "Admis"
            elif 171 <= points < 180:
                resultat = "Repêchable d'office"  # RM8
            elif 153<= points < 171 :
                resultat = "Second tour"
            elif 144 <= points < 153:
                resultat = "Repêchable au 2nd tour"  # RM9
            else:
                resultat = "Échoué"

            # Vérification du repêchage avec la moyenne de cycle (RM7)
            if moyenne_cycle >= 12 and nombre_tentatives <= 2:
                resultat = "Repêchable"  # RM7

            # Si le candidat a fait plus de 2 tentatives, il est automatiquement échoué
            if nombre_tentatives > 2:
                resultat = "Échoué"

            # Insérer les résultats dans la Treeview
            self.tree.insert("", "end", values=(candidat[0], candidat[1], candidat[2], points, resultat))

            # Insérer les résultats dans la table Resultat
            self.cur.execute('''
                INSERT INTO Resultat (numero_table, nom, prenom_s, total_points, decision)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                candidat[0],  # numero_table
                candidat[1],  # nom
                candidat[2],  # prenom_s
                points,  # total_points
                resultat  # decision
            ))

            print(f"Insertion dans Resultat : {candidat[0]}, {candidat[1]}, {candidat[2]}, {points}, {resultat}")
            # Valider la transaction
            self.conn.commit()

    def valider_notes(self, notes):
        """Valide que toutes les notes sont comprises entre 0 et 20."""
        for note in notes:
            if not (0 <= note <= 20):
                raise ValueError("Toutes les notes doivent être comprises entre 0 et 20.")

    def __del__(self):
        """Ferme la connexion à la base de données lorsque la fenêtre est fermée."""
        self.conn.close()
