import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import ttk
import Main
import sys
import threading

# Création de la fenêtre principale
root = tk.Tk()
root.title("Moteur de recherche Python")

# Fonction pour récupérer les valeurs des widgets
class PrintCapture:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)

def animation_chargement(i=0):
    global continuer_animation
    if continuer_animation:
        chargement_label.config(text="Chargement" + "." * i)
        root.update()
        if chargement_label.cget("text") == "Chargement...":
            i = 0
        else:
            i += 1
        root.after(250, animation_chargement, i)

def recherche_thread():
    global continuer_animation
    topic = topic_entry.get()
    mots_cles = mots_cles_entry.get()
    nombre_articles = nombre_articles_spinbox.get()
    methode_affichage = methode_affichage_combobox.get()

    # Appel de la fonction recherche et affichage du résultat de la recherche
    resultat = Main.recherche(topic, mots_cles, nombre_articles, methode_affichage)

    # Restaurer les sorties standard
    sys.stdout = sys.__stdout__

    resultat_text.insert(tk.END, resultat)

    # Arrêter l'animation de chargement
    continuer_animation = False
    chargement_label.config(text="")

def clique_bouton():
    global continuer_animation

    # Démarrer l'animation de chargement
    continuer_animation = True
    animation_chargement()

    # Supprimer le contenu de resultat_text
    resultat_text.delete(1.0, tk.END)

    # Redirection des sorties standard (print) vers resultat_text
    sys.stdout = PrintCapture(resultat_text)

    # Lancer la recherche dans un autre thread
    threading.Thread(target=recherche_thread).start()

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

# Créer un label pour le message de chargement
chargement_label = ttk.Label(root, text="", foreground="red")
# Variable pour contrôler si l'animation doit continuer
continuer_animation = False

# Widget pour afficher le résultat de la recherche
resultat_text = st.ScrolledText(root, width=120, height=35, wrap=tk.WORD)

# Widget pour lancer la recherche
bouton_recherche = ttk.Button(root, text="Rechercher", command=clique_bouton)



# Placement des widgets en utilisant la grille
topic_label.grid(row=0, column=0, sticky="E", padx=10, pady=5)
topic_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)
mots_cles_label.grid(row=1, column=0, sticky="E", padx=10, pady=5)
mots_cles_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)
nombre_articles_label.grid(row=2, column=0, sticky="E", padx=10, pady=5)
nombre_articles_spinbox.grid(row=2, column=1, sticky="w", padx=10, pady=5)
methode_affichage_label.grid(row=3, column=0, sticky="E", padx=10, pady=5)
methode_affichage_combobox.grid(row=3, column=1, sticky="w", padx=10, pady=5)
bouton_recherche.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
chargement_label.grid(row=5, column=0, columnspan=2)
resultat_text.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Lancement de la boucle principale
root.mainloop()