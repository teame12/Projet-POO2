import pandas as pd
import sqlite3

# Lire le fichier Excel
df = pd.read_excel('dossier/BD_BFEM.xlsx', sheet_name='Feuille 1')

#print(df.columns)


# Connexion à la base de données
conn = sqlite3.connect('base_bfem.db')
cur = conn.cursor()

# Insérer les données dans la table Candidat
for index, row in df.iterrows():
    cur.execute('''
        INSERT INTO Candidat (numero_table, prenom_s, nom, date_naissance, lieu_naissance, sexe, nationalite,etablissement,type_candidat,choix_epr_facultative, epreuve_facultative, aptitude_sportive)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?,?,?)
    ''', (
        row['N° de table'],
        row['Prenom (s)'],
        row['NOM'],
        row['Date de nais.'].strftime('%Y-%m-%d'),  # Convertir la date en format YYYY-MM-DD
        row['Lieu de nais.'],
        row['Sexe'],
        row['Nationnallité'],
        row['Etablissement'],
        row['Type de candidat'],
        row['Choix_Épr_Fcultative'] == 'OUT' if 'Choix_Épr_Fcultative' in df.columns else None,  # Convertir en booléen
        row['Epreuve Facultative'],
        row['Etat Sportif'] == 'APTE'  # Convertir en booléen
    ))

# Insérer les données dans la table Livret_Scolaire
for index, row in df.iterrows():
    try:
        # Calcul de la moyenne_cycle si elle n'existe pas déjà
        if 'Moyenne_Cycle' not in df.columns:
            # Calculer la moyenne_cycle en utilisant les moyennes annuelles (6e, 5e, 4e, 3e)
            moyennes_annuelles = [row['Moy_6e'], row['Moy_5e'], row['Moy_4e'], row['Moy_3e']]
            moyennes_annuelles = [moy for moy in moyennes_annuelles if pd.notna(moy)]  # Ignorer les valeurs manquantes
            moyenne_cycle = sum(moyennes_annuelles) / len(moyennes_annuelles) if moyennes_annuelles else None
        else:
            moyenne_cycle = row['Moyenne_Cycle']

        # Insertion des données dans la table Livret_Scolaire
        cur.execute('''
            INSERT INTO Livret_Scolaire (numero_table, nombre_de_fois, moyenne_6e, moyenne_5e, moyenne_4e, moyenne_3e, moyenne_Cycle)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['N° de table'],  # numero_table
            row['Nb fois'],      # nombre_de_fois
            row['Moy_6e'] if pd.notna(row['Moy_6e']) else None,  # moyenne_6e (gestion des valeurs manquantes)
            row['Moy_5e'] if pd.notna(row['Moy_5e']) else None,  # moyenne_5e
            row['Moy_4e'] if pd.notna(row['Moy_4e']) else None,  # moyenne_4e
            row['Moy_3e'] if pd.notna(row['Moy_3e']) else None,  # moyenne_3e
            moyenne_cycle  # moyenne_Cycle (calculée ou existante)
        ))

        # Valider la transaction
        conn.commit()

    except Exception as e:
        # En cas d'erreur, annuler la transaction et afficher un message d'erreur
        conn.rollback()
        print(f"Erreur lors de l'insertion de la ligne {index + 1} : {e}")

# Insérer les données dans la table Notes
for index, row in df.iterrows():

    cur.execute('''
        INSERT INTO Notes (numero_table, compo_franc, coef1, dictee, coef2, etude_de_texte, coef3, instruction_Civique, coef4, histoire_Geographie, coef5, mathematiques, coef6, pc_lv2, coef7, SVT, coef8, anglais1, coef9, anglais_oral, coef10, eps, epreuve_facultative)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['N° de table'],  # idCandidat
        row['Note CF'],  # compo_franc
        2,  # coef1
        row['Note Ort'],  # dictee
        1,  # coef2
        row['Note TSQ'],  # etude_de_texte
        1,  # coef3
        row['Note IC'],  # instruction_Civique
        1,  # coef4
        row['Note HG'],  # histoire_Geographie
        2,  # coef5
        row['Note MATH'],  # mathematiques
        4,  # coef6
        row['Note PC/LV2'],  # pc_lv2
        2,  # coef7
        row['Note SVT'],  # SVT
        2,  # coef8
        row['Note ANG1'],  # anglais1
        2,  # coef9
        row['Note ANG2'],  # anglais_oral
        1,  # coef10
        row['Note EPS'],  # eps
        row['Note Ep Fac']  # epreuve_facultative
    ))

# Valider la transaction
conn.commit()

# Fermer la connexion
conn.close()