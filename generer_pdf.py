from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import sqlite3
from tkinter import messagebox

from anonymat import generer_anonymat


def generate_pdf(filename, title, data, columns, jury_info=None):
    """Génère un PDF stylisé avec un tableau et des informations optionnelles du jury."""
    try:
        # Utiliser une orientation paysage pour plus d'espace horizontal
        doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
        elements = []
        styles = getSampleStyleSheet()

        # Ajouter un titre au PDF
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 12))  # Espacement entre le titre et le tableau

        # Ajouter les informations du jury si elles sont fournies
        if jury_info:
            elements.append(Paragraph("Informations du Jury", styles['Heading2']))
            elements.append(Spacer(1, 8))
            details_jury = [
                f"Région: {jury_info[0]}",
                f"Département: {jury_info[1]}",
                f"Localité: {jury_info[2]}",
                f"Centre d'examen: {jury_info[3]}",
                f"Président du jury: {jury_info[4]}"
            ]
            for info in details_jury:
                elements.append(Paragraph(info, styles['Normal']))
            elements.append(Spacer(1, 12))

        # Fractionner les données si elles sont trop grandes pour une seule page
        max_rows_per_page = 25
        for i in range(0, len(data), max_rows_per_page):
            chunk = data[i:i+max_rows_per_page]
            table_data = [columns] + chunk

            # Créer le tableau avec un style amélioré
            table = Table(table_data, colWidths=[80] + [120] * (len(columns) - 1))
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 2, colors.black)
            ]))

            elements.append(table)
            elements.append(PageBreak())

        doc.build(elements)
        print(f"PDF généré avec succès : {filename}")

    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")

def fetch_data(query):
    """Exécute une requête SQL et retourne les résultats."""
    conn = sqlite3.connect("base_bfem.db")
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur SQL : {e}")
        return []
    finally:
        conn.close()

def fetch_jury_info():
    """Récupère les informations du jury."""
    conn = sqlite3.connect("base_bfem.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT region, departement, localite, centre_examen, president_jury FROM Jury LIMIT 1''')
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur SQL lors de la récupération du jury : {e}")
        return None
    finally:
        conn.close()

def generate_candidats_pdf():
    """Génère le PDF des candidats."""
    data = fetch_data("SELECT numero_table, nom, prenom_s, date_naissance, lieu_naissance, etablissement, type_candidat FROM Candidat ORDER BY nom")
    columns = ["Numéro Table", "Nom", "Prénom", "Date de naissance", "Lieu de naissance", "Établissement", "Type"]
    generate_pdf("liste_candidats.pdf", "Liste des Candidats", data, columns, fetch_jury_info())

def generate_anonymats_pdf():
    """Génère le PDF des anonymats."""
    data = fetch_data("SELECT numero_table, anonymatPrincipal FROM AnonymatPrincipal ORDER BY numero_table")
    columns = ["Numéro Table", "Code Anonymat"]
    generate_pdf("anonymats.pdf", "Liste des Anonymats", data, columns, fetch_jury_info())

def generate_pv_pdf():
    """Génère le PDF des PV des résultats."""
    data = fetch_data("SELECT numero_table, nom, prenom_s, total_points, decision FROM Resultat ORDER BY nom")
    columns = ["Numéro Table", "Nom", "Prénom", "Total Points", "Décision"]
    generate_pdf("proces_verbal.pdf", "Procès-Verbal des Résultats", data, columns, fetch_jury_info())

def generate_resultats_pdf():
    """Génère les PDF des admis au 1er et 2nd tour."""
    # Admis au 1er tour, incluant ceux repêchés d'office
    data_1er_tour = fetch_data('''SELECT numero_table, nom, prenom_s, total_points FROM Resultat WHERE decision = "Admis" OR decision = "Repêchable d''office" ORDER BY total_points DESC ''')
    columns_1er_tour = ["Numéro Table", "Nom", "Prénom", "Points"]
    generate_pdf("resultats_admis_1er_tour.pdf", "Liste des Admis au 1er Tour", data_1er_tour, columns_1er_tour)

    # Admis au 2nd tour
    data_2nd_tour = fetch_data('''SELECT numero_table, nom, prenom_s, total_points FROM Resultat WHERE decision = "Second tour" OR decision = "Repêchable au 2nd tour" ORDER BY total_points DESC''')
    columns_2nd_tour = ["Numéro Table", "Nom", "Prénom", "Points"]
    generate_pdf("resultats_admis_2nd_tour.pdf", "Liste des Admis au 2nd Tour", data_2nd_tour, columns_2nd_tour)


def generer_tous_les_pdfs():
    """Génère tous les PDF et affiche un message de confirmation."""
    try:
        generate_candidats_pdf()
        generate_anonymats_pdf()
        generate_pv_pdf()
        generate_resultats_pdf()
        messagebox.showinfo("Succès", "Tous les PDF ont été générés avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
