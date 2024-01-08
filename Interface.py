import tkinter as tk
from tkinter import ttk
import Main
import sys

# Création de la fenêtre principale
root = tk.Tk()
root.title("Moteur de recherche Python")

# Fonction pour récupérer les valeurs des widgets
class PrintCapture:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)

def clique_bouton():
    topic = topic_entry.get()
    mots_cles = mots_cles_entry.get()
    nombre_articles = nombre_articles_spinbox.get()
    methode_affichage = methode_affichage_combobox.get()
    
    # Supprimer le contenu de resultat_text
    resultat_text.delete(1.0, tk.END)

    # Redirect print statements to the text widget
    sys.stdout = PrintCapture(resultat_text)

    # Appel de la fonction recherche et affichage du résultat de la recherche
    resultat = Main.recherche(topic, mots_cles, nombre_articles, methode_affichage)

    # Restore the standard output
    sys.stdout = sys.__stdout__

    resultat_text.insert(tk.END, resultat)

# Widgets pour saisir le topic de la recherche
topic_label = ttk.Label(root, text="Topic")
topic_entry = ttk.Entry(root)
topic_entry.insert(0, "Space")

# Widgets pour saisir les mots-clés de la recherche
mots_cles_label = ttk.Label(root, text="Mots clés")
mots_cles_entry = ttk.Entry(root)
mots_cles_entry.insert(0, "Space Moon")

# Widgets pour sélectionner le nombre d'articles à extraire
nombre_articles_label = ttk.Label(root, text="Nombre d'articles à extraire")
nombre_articles_spinbox = ttk.Spinbox(root, from_=1, to=1000)
nombre_articles_spinbox.insert(0, 100)

# Widgets pour choisir la méthode d'affichage des résultats
methode_affichage_label = ttk.Label(root, text="Méthode d'affichage")
methode_affichage_combobox = ttk.Combobox(root, values=['Pertinence', 'Temporelle', 'Alphabétique'])
methode_affichage_combobox.set('Pertinence')

# Widget pour afficher le résultat de la recherche
resultat_text = tk.Text(root)

# Widget pour lancer la recherche
bouton_recherche = ttk.Button(root, text="Rechercher", command=clique_bouton)

# Placement des widgets en utilisant la grille
topic_label.grid(row=0, column=0, sticky="w", padx=50)
topic_entry.grid(row=0, column=1, padx=5, pady=5)
mots_cles_label.grid(row=1, column=0, sticky="w", padx=50)
mots_cles_entry.grid(row=1, column=1, padx=5, pady=5)
nombre_articles_label.grid(row=2, column=0, sticky="w", padx=50)
nombre_articles_spinbox.grid(row=2, column=1, padx=5, pady=5)
methode_affichage_label.grid(row=3, column=0, sticky="w", padx=50)
methode_affichage_combobox.grid(row=3, column=1, padx=5, pady=5)
bouton_recherche.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
resultat_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Lancement de la boucle principale
root.mainloop()