import sqlite3
import tkinter
from tkinter import *
import matplotlib.pyplot as plt

class FormulaireStatistique:
    def __init__(self, parent):
        self.fenetre = tkinter.Toplevel(parent)
        self.fenetre.title("Statistiques")
        self.fenetre.geometry("600x600")
        self.fenetre.configure(bg="#87CEFA")

        # Labels pour afficher les statistiques
        self.label_admis = Label(self.fenetre, text="Admis: 0 (0%)", bg="#87CEFA", fg="white", font=("Arial", 14, "bold"))
        self.label_admis.pack(pady=10)

        self.label_repeches_office = Label(self.fenetre, text="Repêchés d’office: 0 (0%)", bg="#87CEFA", fg="white", font=("Arial", 14, "bold"))
        self.label_repeches_office.pack(pady=10)

        self.label_repeches_second_tour = Label(self.fenetre, text="Repêchés au second tour: 0 (0%)", bg="#87CEFA", fg="white", font=("Arial", 14, "bold"))
        self.label_repeches_second_tour.pack(pady=10)

        self.label_second_tour = Label(self.fenetre, text="Second tour: 0 (0%)", bg="#87CEFA", fg="white", font=("Arial", 14, "bold"))
        self.label_second_tour.pack(pady=10)

        self.label_repechable = Label(self.fenetre, text="Repêchable: 0 (0%)", bg="#87CEFA", fg="white", font=("Arial", 14, "bold"))
        self.label_repechable.pack(pady=10)

        self.label_echoues = Label(self.fenetre, text="Échoués: 0 (0%)", bg="#87CEFA", fg="white", font=("Arial", 14, "bold"))
        self.label_echoues.pack(pady=10)

        # Bouton pour calculer les statistiques
        Button(self.fenetre, text="Calculer les statistiques", bg="#4682B4", fg="white", font=("Arial", 14, "bold"), command=self.calculer_statistiques).pack(pady=10)

        # Connexion à la base de données
        self.conn = sqlite3.connect('base_bfem.db')
        self.cur = self.conn.cursor()

    def calculer_statistiques(self):
        """Calcule et affiche les statistiques des candidats."""
        try:
            self.cur.execute('''SELECT COUNT(*) FROM Resultat''')
            total_candidats = self.cur.fetchone()[0]

            if total_candidats == 0:
                print("Aucun candidat trouvé dans la table Resultat.")
                return

            self.cur.execute('''SELECT COUNT(*) FROM Resultat WHERE decision = "Admis"''')
            admis = self.cur.fetchone()[0]

            self.cur.execute('''SELECT COUNT(*) FROM Resultat WHERE decision = "Repêchable d'office"''')
            repeches_office = self.cur.fetchone()[0]

            self.cur.execute('''SELECT COUNT(*) FROM Resultat WHERE decision = "Repêchable au 2nd tour"''')
            repeches_second_tour = self.cur.fetchone()[0]

            self.cur.execute('''SELECT COUNT(*) FROM Resultat WHERE decision = "Second tour"''')
            second_tour = self.cur.fetchone()[0]

            self.cur.execute('''SELECT COUNT(*) FROM Resultat WHERE decision = "Repêchable"''')
            repechable = self.cur.fetchone()[0]

            self.cur.execute('''SELECT COUNT(*) FROM Resultat WHERE decision = "Échoué"''')
            echoues = self.cur.fetchone()[0]

            def calcul_pourcentage(nombre):
                return (nombre / total_candidats) * 100 if total_candidats > 0 else 0

            pourcentage_admis = calcul_pourcentage(admis)
            pourcentage_repeches_office = calcul_pourcentage(repeches_office)
            pourcentage_repeches_second_tour = calcul_pourcentage(repeches_second_tour)
            pourcentage_second_tour = calcul_pourcentage(second_tour)
            pourcentage_repechable = calcul_pourcentage(repechable)
            pourcentage_echoues = calcul_pourcentage(echoues)

            self.label_admis.config(text=f"Admis: {admis} ({pourcentage_admis:.2f}%)")
            self.label_repeches_office.config(text=f"Repêchés d’office: {repeches_office} ({pourcentage_repeches_office:.2f}%)")
            self.label_repeches_second_tour.config(text=f"Repêchés au second tour: {repeches_second_tour} ({pourcentage_repeches_second_tour:.2f}%)")
            self.label_second_tour.config(text=f"Second tour: {second_tour} ({pourcentage_second_tour:.2f}%)")
            self.label_repechable.config(text=f"Repêchable: {repechable} ({pourcentage_repechable:.2f}%)")
            self.label_echoues.config(text=f"Échoués: {echoues} ({pourcentage_echoues:.2f}%)")

            # Affichage du diagramme circulaire
            self.afficher_diagramme(admis, repeches_office, repeches_second_tour, second_tour, repechable, echoues)

        except sqlite3.Error as e:
            print(f"Erreur SQL lors du calcul des statistiques : {e}")

    def afficher_diagramme(self, admis, repeches_office, repeches_second_tour, second_tour, repechable, echoues):
        labels = ['Admis', 'Repêchés d’office', 'Repêchés au second tour', 'Second tour', 'Repêchable', 'Échoués']
        sizes = [admis, repeches_office, repeches_second_tour, second_tour, repechable, echoues]
        colors = ['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0', '#F44336']
        explode = (0.1, 0, 0, 0, 0, 0)  # Mettre en évidence le premier morceau ('Admis')

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Assurer que le diagramme est bien circulaire
        plt.title("Répartition des Résultats des Candidats")
        plt.show()

    def __del__(self):
        self.conn.close()

