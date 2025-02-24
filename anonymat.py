import sqlite3
import uuid

# Liste des épreuves
epreuves = ["compo_franc", "dictee", "etude_texte", "instruction_civique", "histoire_geographie", "mathematiques", "pc_lv2", "svt", "anglais1", "anglais_oral", "eps", "epreuve_facultative"]

def generer_anonymat(prefixe):
    """Génère un numéro d'anonymat unique avec un préfixe."""
    return f"{prefixe}_{str(uuid.uuid4().hex)[:8]}"

def enregistrer_anonymat_principal(id_candidat):
    """Enregistre un anonymat principal pour un candidat."""
    conn = sqlite3.connect('base_bfem.db')
    cur = conn.cursor()
    try:
        # Vérifier si un anonymat principal existe déjà
        cur.execute('''
                    SELECT anonymatPrincipal FROM AnonymatPrincipal
                    WHERE numero_table = ?
                ''', (id_candidat,))
        resultat = cur.fetchone()

        #si l'anonymat existe deja le retouner
        if resultat :
            #print(f"Anonymat principal déjà existant pour le candidat {id_candidat}: {resultat[0]}")
            return resultat[0]

        #sinon générer un anonymat principal unique et l'ajouter dans la table
        anonymat_principal = generer_anonymat("PRINCIPAL")
        cur.execute('''
            INSERT INTO AnonymatPrincipal (numero_table, anonymatPrincipal)
            VALUES (?, ?)
        ''', (id_candidat, anonymat_principal))
        conn.commit()
        return anonymat_principal
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'anonymat principal pour le candidat {id_candidat} : {e}")
        return None
    finally:
        conn.close()

def enregistrer_anonymat_epreuve(id_anonymat, epreuve):
    """Enregistre un anonymat pour une épreuve."""
    conn = sqlite3.connect('base_bfem.db')
    cur = conn.cursor()
    try:
        # Vérifier si un anonymat existe déjà pour cette épreuve et ce candidat
        cur.execute('''
                   SELECT anonymatEpreuve FROM AnonymatEpreuve
                   WHERE idAnonymat = ? AND epreuve = ?
               ''', (id_anonymat, epreuve))
        resultat = cur.fetchone()

        # Si l'anonymat existe déjà, le retourner
        if resultat:
            #print(f"Anonymat déjà existant pour {epreuve}: {resultat[0]}")
            return resultat[0]

        #sinon générer un anonymat unique pour l'épreuve
        anonymat_epreuve = generer_anonymat(epreuve)
        cur.execute('''
            INSERT INTO AnonymatEpreuve (idAnonymat, epreuve, anonymatEpreuve)
            VALUES (?, ?, ?)
        ''', (id_anonymat, epreuve, anonymat_epreuve))
        conn.commit()
        return anonymat_epreuve
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'anonymat pour l'épreuve {epreuve} : {e}")
        return None
    finally:
        conn.close()

def generer_anonymats_pour_tous_les_candidats():
    """Génère les anonymats pour tous les candidats et toutes les épreuves."""
    conn = sqlite3.connect('base_bfem.db')
    cur = conn.cursor()
    try:
        # Récupérer tous les candidats de la table Candidat
        cur.execute('''SELECT numero_table FROM Candidat''')
        candidats = cur.fetchall()

        # Générer les anonymats pour chaque candidat
        for candidat in candidats:
            id_candidat = candidat[0]

            # Enregistrer l'anonymat principal
            anonymat_principal = enregistrer_anonymat_principal(id_candidat)
            if anonymat_principal:
                # Récupérer l'ID de l'anonymat principal
                cur.execute('''SELECT idAnonymat FROM AnonymatPrincipal WHERE anonymatPrincipal = ?''', (anonymat_principal,))
                id_anonymat = cur.fetchone()[0]

                # Enregistrer les anonymats pour chaque épreuve
                for epreuve in epreuves:
                    enregistrer_anonymat_epreuve(id_anonymat, epreuve)
    except Exception as e:
        print(f"Erreur lors de la génération des anonymats : {e}")
    finally:
        conn.close()

def recuperer_anonymat_principal(id_candidat):
    """Récupère l'anonymat principal d'un candidat."""
    conn = sqlite3.connect('base_bfem.db')
    cur = conn.cursor()
    try:
        cur.execute('''SELECT anonymatPrincipal FROM AnonymatPrincipal WHERE numero_table = ?''', (id_candidat,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'anonymat principal : {e}")
        return None
    finally:
        conn.close()

def recuperer_anonymats_epreuves(id_candidat):
    """Récupère les anonymats des épreuves d'un candidat."""
    conn = sqlite3.connect('base_bfem.db')
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT epreuve, anonymatEpreuve
            FROM AnonymatEpreuve
            JOIN AnonymatPrincipal ON AnonymatEpreuve.idAnonymat = AnonymatPrincipal.idAnonymat
            WHERE AnonymatPrincipal.numero_table = ?
        ''', (id_candidat,))
        return cur.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des anonymats des épreuves : {e}")
        return []
    finally:
        conn.close()

# Générer les anonymats pour tous les candidats
generer_anonymats_pour_tous_les_candidats()