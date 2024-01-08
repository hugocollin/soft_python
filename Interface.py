import tkinter as tk
from tkinter import ttk
import Main

# Création de la fenêtre principale
root = tk.Tk()
root.title("Moteur de recherche Python")

# Fonction pour récupérer les valeurs des widgets
def clique_bouton():
    topic = topic_entry.get()
    mots_cles = mots_cles_entry.get()
    nombre_articles = nombre_articles_spinbox.get()
    methode_affichage = methode_affichage_combobox.get()
    
    # Appel de la fonction recherche et affichage du résultat de la recherche
    resultat = Main.recherche(topic, mots_cles, nombre_articles, methode_affichage)
    resultat_text.delete(1.0, tk.END)
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

# Placement des widgets
topic_label.pack()
topic_entry.pack()
mots_cles_label.pack()
mots_cles_entry.pack()
nombre_articles_label.pack()
nombre_articles_spinbox.pack()
methode_affichage_label.pack()
methode_affichage_combobox.pack()
bouton_recherche.pack()
resultat_text.pack()

# Lancement de la boucle principale
root.mainloop()