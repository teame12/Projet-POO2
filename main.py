import tkinter as tk
from formulaire_candidat1 import FormulaireCandidat
from formulaire_notes import FormulaireNotes
from deliberation import FormulaireDeliberation
from generer_releves import FormulaireReleveNotes
from jury import FormulaireJury
from statistiques import FormulaireStatistique
from generer_pdf import generer_tous_les_pdfs

# 🌊 Couleurs bleu ciel
BG_COLOR = "#B0E0E6"  # Bleu ciel clair
BTN_COLOR = "#4682B4"  # Bleu acier
BTN_HOVER = "#5F9EA0"  # Bleu turquoise
TEXT_COLOR = "#ffffff"  # Blanc

#Créer la fenêtre principale
root = tk.Tk()
root.title("Gestion des candidats au BFEM")
root.geometry("800x600")
root.configure(bg=BG_COLOR)

#En-tête stylisé
header = tk.Label(root, text="Gestion des Candidats au BFEM",
                  font=("Arial", 18, "bold"), bg=BTN_COLOR, fg="white", pady=15)
header.pack(fill="x")


#Création des boutons avec un peu plus de style
def create_button(text, command):
    btn = tk.Button(root, text=text, font=("Arial", 14, "bold"),
                    bg=BTN_COLOR, fg=TEXT_COLOR, bd=3, relief="raised",
                    padx=10, pady=10, width=30, command=command)
    btn.pack(pady=10)

    # Ajout de l'effet hover
    #btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
    #btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))


#Ajouter les boutons
create_button("🎓 Paramétrer le jury", lambda: FormulaireJury(root))
create_button("📝 Enregistrer un candidat", lambda: FormulaireCandidat(root))
create_button("📊 Notes", lambda: FormulaireNotes(root))
create_button("⚖ Délibération", lambda: FormulaireDeliberation(root))
create_button("generer les pdfs", generer_tous_les_pdfs)
create_button("📈 Statistiques", lambda: FormulaireStatistique(root))
create_button("📜 Générer Relevé de Notes", lambda: FormulaireReleveNotes(root))

#Lancer la boucle principale de l'interface
root.mainloop()