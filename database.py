import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('base_bfem.db')
cur = conn.cursor()

# Création de la table Candidat
cur.execute('''CREATE TABLE IF NOT EXISTS Candidat (
    numero_table INTEGER PRIMARY KEY,
    prenom_s TEXT NOT NULL,
    nom TEXT NOT NULL,
    date_naissance DATE NOT NULL,
    lieu_naissance TEXT NOT NULL,
    sexe CHAR(1) NOT NULL,
    nationalite TEXT NOT NULL,
    etablissement TEXT NOT NULL,
    type_candidat TEXT NOT NULL,
    choix_epr_facultative BOOLEAN,
    epreuve_facultative TEXT,
    aptitude_sportive BOOLEAN NOT NULL
)''')

# Création de la table Livret_Scolaire
cur.execute('''CREATE TABLE IF NOT EXISTS Livret_Scolaire (
    idLivretScolaire INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_table INTEGER NOT NULL,
    nombre_de_fois INTEGER NOT NULL,
    moyenne_6e DECIMAL(4, 2),
    moyenne_5e DECIMAL(4, 2),
    moyenne_4e DECIMAL(4, 2),
    moyenne_3e DECIMAL(4, 2),
    moyenne_Cycle DECIMAL(4, 2),
    FOREIGN KEY (numero_table) REFERENCES Candidat(numero_table))
''')

# Création de la table Notes
cur.execute('''CREATE TABLE IF NOT EXISTS Notes (
    idNotes INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_table INTEGER NOT NULL,
    compo_franc DECIMAL(4, 2),
    coef1 INTEGER NOT NULL,
    dictee DECIMAL(4, 2),
    coef2 INTEGER NOT NULL,
    etude_de_texte DECIMAL(4, 2),
    coef3 INTEGER NOT NULL,
    instruction_Civique DECIMAL(4, 2),
    coef4 INTEGER NOT NULL,
    histoire_Geographie DECIMAL(4, 2),
    coef5 INTEGER NOT NULL,
    mathematiques DECIMAL(4, 2),
    coef6 INTEGER NOT NULL,
    pc_lv2 DECIMAL(4, 2),
    coef7 INTEGER NOT NULL,
    SVT DECIMAL(4, 2),
    coef8 INTEGER NOT NULL,
    anglais1 DECIMAL(4, 2),
    coef9 INTEGER NOT NULL,
    anglais_oral DECIMAL(4, 2),
    coef10 INTEGER NOT NULL,
    eps DECIMAL(4, 2),
    epreuve_facultative DECIMAL(4, 2),
    FOREIGN KEY (numero_table) REFERENCES Candidat(numero_table))
''')

# Création de la table Jury
cur.execute('''CREATE TABLE IF NOT EXISTS Jury (
    idJury INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL,
    departement TEXT NOT NULL,
    localite TEXT NOT NULL,
    centre_examen TEXT NOT NULL,
    president_jury TEXT NOT NULL,
    telephone TEXT NOT NULL
)''')

# Création de la table Anonymat
"""cur.execute('''
    CREATE TABLE IF NOT EXISTS Anonymat (
        idAnonymat INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_table INTEGER NOT NULL,
        numero_anonymat TEXT NOT NULL UNIQUE,
        epreuve TEXT NOT NULL,
        principal TEXT,
        FOREIGN KEY (numero_table) REFERENCES Candidat(numero_table)
    )
''')"""

cur.execute('''CREATE TABLE IF NOT EXISTS Resultat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_table INTEGER NOT NULL,
    nom TEXT NOT NULL,
    prenom_s TEXT NOT NULL,
    total_points REAL NOT NULL,
    decision TEXT NOT NULL,
    FOREIGN KEY (numero_table) REFERENCES Candidat(numero_table)
)''')

# Création de la table Notes_2nd_Tour
cur.execute('''CREATE TABLE IF NOT EXISTS Notes_2nd_Tour (
    idNotes2ndTour INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_table INTEGER NOT NULL,
    francais DECIMAL(4, 2),
    coefA INTEGER NOT NULL,
    mathematiques DECIMAL(4, 2),
    coefB INTEGER NOT NULL,
    pc_lv2 DECIMAL(4, 2),
    coefC INTEGER NOT NULL,
    FOREIGN KEY (numero_table) REFERENCES Candidat(numero_table)
)''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS AnonymatPrincipal (
                idAnonymat INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_table INTEGER,
                anonymatPrincipal TEXT UNIQUE,
                FOREIGN KEY (numero_table) REFERENCES Candidat(numero_table)
            )
''')

# Table pour les anonymats des épreuves
cur.execute('''
    CREATE TABLE IF NOT EXISTS AnonymatEpreuve (
        idAnonymatEpreuve INTEGER PRIMARY KEY AUTOINCREMENT,
        idAnonymat INTEGER,
        epreuve TEXT,
        anonymatEpreuve TEXT UNIQUE,
        FOREIGN KEY (idAnonymat) REFERENCES AnonymatPrincipal(idAnonymat)
    )
''')

# Validation de la transaction
conn.commit()

# Fermeture de la connexion
conn.close()