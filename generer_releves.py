import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import sqlite3

class FormulaireReleveNotes:
    def __init__(self, parent):
        self.fenetre = tk.Toplevel(parent)
        self.fenetre.title("Générateur de relevés de notes")
        self.fenetre.geometry("800x600")
        self.fenetre.configure(bg="#87CEFA")

        # Connexion à la base de données
        self.conn = sqlite3.connect('base_bfem.db')
        self.cur = self.conn.cursor()

        # Interface graphique
        self.creer_interface()

    def creer_interface(self):
        # Frame pour la sélection du candidat
        frame_selection = tk.Frame(self.fenetre, bg="#87CEFA")
        frame_selection.pack(pady=10)

        # Label et Combobox pour sélectionner un candidat
        tk.Label(frame_selection, text="Sélectionner un candidat :", bg="#87CEFA").grid(row=0, column=0, padx=10, pady=10)
        self.combo_candidat = ttk.Combobox(frame_selection, width=50)
        self.combo_candidat.grid(row=0, column=1, padx=10, pady=10)
        self.combo_candidat.bind("<<ComboboxSelected>>", self.afficher_notes)

        # Remplir la liste déroulante avec les candidats
        self.remplir_liste_candidats()

        # Frame pour afficher les notes
        frame_notes = tk.Frame(self.fenetre, bg="#87CEFA")
        frame_notes.pack(pady=10)

        # Treeview pour afficher les notes du 1er tour
        self.tree_1er_tour = ttk.Treeview(frame_notes, columns=("Épreuve", "Note", "Coefficient", "Points"), show="headings")
        self.tree_1er_tour.heading("Épreuve", text="Épreuve")
        self.tree_1er_tour.heading("Note", text="Note")
        self.tree_1er_tour.heading("Coefficient", text="Coefficient")
        self.tree_1er_tour.heading("Points", text="Points")
        self.tree_1er_tour.pack(side=tk.LEFT, padx=10, pady=10)

        # Bouton pour générer le relevé de notes
        tk.Button(self.fenetre, text="Générer le relevé de notes", command=self.generer_releve_pdf, bg="#4682B4", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    def remplir_liste_candidats(self):
        """Remplit la liste déroulante avec les candidats de la base de données."""
        self.cur.execute("SELECT numero_table, nom, prenom_s FROM Candidat")
        candidats = self.cur.fetchall()
        self.combo_candidat['values'] = [f"{c[0]} - {c[1]} {c[2]}" for c in candidats]

    def afficher_notes(self, event):
        """Affiche les notes du candidat sélectionné pour le 1er tour."""
        # Récupérer l'ID du candidat sélectionné

        selected_candidate = self.combo_candidat.get()
        numero_table = selected_candidate.split(" - ")[0]

        # Vider les Treeview avant d'afficher de nouvelles données
        for row in self.tree_1er_tour.get_children():
            self.tree_1er_tour.delete(row)

        self.cur.execute("SELECT aptitude_sportive FROM Candidat WHERE numero_table = ?", (numero_table,))
        aptitude_sportive = self.cur.fetchone()[0]

        # Récupérer les notes du 1er tour
        self.cur.execute('''
            SELECT compo_franc, dictee, etude_de_texte, instruction_Civique, histoire_Geographie,
                   mathematiques, pc_lv2, SVT, anglais1, anglais_oral, eps, epreuve_facultative
            FROM Notes
            WHERE numero_table = ?
        ''', (numero_table,))
        notes_1er_tour = self.cur.fetchone()

        # Afficher les notes du 1er tour
        if notes_1er_tour:
            epreuves_1er_tour = [
                ("Composition Française", notes_1er_tour[0], 2),
                ("Dictée", notes_1er_tour[1], 1),
                ("Étude de texte", notes_1er_tour[2], 1),
                ("Instruction Civique", notes_1er_tour[3], 1),
                ("Histoire-Géographie", notes_1er_tour[4], 2),
                ("Mathématiques", notes_1er_tour[5], 4),
                ("PC/LV2", notes_1er_tour[6], 2),
                ("SVT", notes_1er_tour[7], 2),
                ("Anglais écrit", notes_1er_tour[8], 2),
                ("Anglais oral", notes_1er_tour[9], 1),
                ("EPS", notes_1er_tour[10], 1),
                ("Épreuve facultative", notes_1er_tour[11], 1)
            ]
            for epreuve, note, coef in epreuves_1er_tour:
                # Vérifier si la note est None
                if note is None:
                    note = 0  # Remplacer None par 0

                if epreuve == "EPS":
                    if aptitude_sportive == 1:
                        if note > 10:
                            points = f"+{note - 10}"
                        elif note < 10:
                            points = f"-{10 - note}"
                        else:
                            points = 0
                    else:
                        points = 0

                elif epreuve == "Épreuve facultative":
                    if note > 10:
                        points = f"+{note - 10}"
                    else:
                        points = 0
                else:
                    points = note * coef
                self.tree_1er_tour.insert("", "end", values=(epreuve, note, coef, points))

    def generer_releve_pdf(self):
        """Génère un relevé de notes au format PDF pour le candidat sélectionné."""
        global points
        selected_candidate = self.combo_candidat.get()
        if not selected_candidate:
            messagebox.showerror("Erreur", "Veuillez sélectionner un candidat.")
            return

        numero_table = selected_candidate.split(" - ")[0]

        # Récupérer les informations du candidat
        self.cur.execute('''
            SELECT nom, prenom_s, date_naissance, lieu_naissance,etablissement, aptitude_sportive
            FROM Candidat WHERE numero_table = ?
        ''', (numero_table,))
        candidat_info = self.cur.fetchone()
        if not candidat_info:
            messagebox.showerror("Erreur", "Candidat non trouvé.")
            return

        nom, prenom, date_naissance, lieu_naissance,etablissement, aptitude_sportive = candidat_info

        # Récupérer les résultats de la table Resultat
        self.cur.execute('''
            SELECT total_points, decision
            FROM Resultat
            WHERE numero_table = ?
        ''', (numero_table,))
        resultat_info = self.cur.fetchone()
        if not resultat_info:
            messagebox.showerror("Erreur", "Résultats non trouvés pour ce candidat.")
            return

        total_points, decision = resultat_info

        # Calculer la moyenne (si nécessaire)
        total_coef = 20  # Exemple : total des coefficients
        moyenne = total_points / total_coef if total_coef > 0 else 0

        # Générer le PDF
        filename = f"releve_notes_{nom}_{prenom}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Titre du relevé
        elements.append(Paragraph("RELEVE DE NOTES DU 1ER GROUPE D'EPREUVES", styles['Title']))
        elements.append(Spacer(1, 12))

        # Informations du candidat
        elements.append(Paragraph(f"Nom: {nom}", styles['Normal']))
        elements.append(Paragraph(f"Prénom(s): {prenom}", styles['Normal']))
        elements.append(Paragraph(f"Date de naissance: {date_naissance}", styles['Normal']))
        elements.append(Paragraph(f"Lieu de naissance: {lieu_naissance}", styles['Normal']))
        elements.append(Paragraph(f"Etablissement: {etablissement}", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Tableau des notes (vous pouvez récupérer les notes individuelles si nécessaire)
        data = [["Épreuve", "Note", "Coefficient", "Points"]]
        # Exemple : Récupérer les notes individuelles si nécessaire
        self.cur.execute('''
            SELECT compo_franc, dictee, etude_de_texte, instruction_Civique, histoire_Geographie,
                   mathematiques, pc_lv2, SVT, anglais1, anglais_oral, eps, epreuve_facultative
            FROM Notes
            WHERE numero_table = ?
        ''', (numero_table,))
        notes_1er_tour = self.cur.fetchone()

        if notes_1er_tour:
            epreuves_1er_tour = [
                ("Composition Française", notes_1er_tour[0], 2),
                ("Dictée", notes_1er_tour[1], 1),
                ("Étude de texte", notes_1er_tour[2], 1),
                ("Instruction Civique", notes_1er_tour[3], 1),
                ("Histoire-Géographie", notes_1er_tour[4], 2),
                ("Mathématiques", notes_1er_tour[5], 4),
                ("PC/LV2", notes_1er_tour[6], 2),
                ("SVT", notes_1er_tour[7], 2),
                ("Anglais écrit", notes_1er_tour[8], 2),
                ("Anglais oral", notes_1er_tour[9], 1),
                ("EPS", notes_1er_tour[10], 1),
                ("Épreuve facultative", notes_1er_tour[11], 1)
            ]
            for epreuve, note, coef in epreuves_1er_tour:
                if note is None:
                    note = 0  # Remplacer None par 0

                if epreuve == "EPS":
                    if aptitude_sportive == 1:
                        if note > 10:
                            points = f"+{note - 10}"
                        elif note < 10:
                            points = f"-{10 - note}"
                        else:
                            points = 0
                    else:
                        points = 0

                elif epreuve == "Épreuve facultative":
                    if note > 10:
                        points = f"+{note - 10}"
                    else:
                        points = 0
                else:
                    points = note * coef
                data.append([epreuve, note, coef, points])



                #print(f"{epreuve} | Note: {note} | Coef: {coef} | Points: {points}")

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        # Tableau pour les totaux, moyenne, coefficients et décision
        tyles = getSampleStyleSheet()
        style_title = styles['Title']
        style_normal = styles['Normal']

        # Contenu formaté
        total_text = f"""
            <b>Totaux (A) :</b> {total_points} sur 360<br/>
            <b>Moyenne Globale (A) :</b> {moyenne:.2f} sur 20<br/>
            <b>Décision du jury :</b> {decision}
        """

        # Créer un paragraphe stylisé
        total_paragraph = Paragraph(total_text, style_normal)

        # Ajouter au document
        elements.append(total_paragraph)
        # Générer le PDF
        doc.build(elements)
        messagebox.showinfo("Succès", f"Relevé de notes généré : {filename}")

    def __del__(self):
        """Ferme la connexion à la base de données lorsque la fenêtre est fermée."""
        self.conn.close()