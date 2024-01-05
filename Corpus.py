from Document import RedditDocument, ArxivDocument # Importation de la classe RedditDocument et ArxivDocument depuis le module Document
from Author import Author                          # Importation de la classe Author depuis le module Author

import re           # Importation de la bibliotheque re, afin de travailler avec des expressions régulières
import pandas as pd # Importation de la bibliotheque pandas, afin de manipuler et d'analyser des données

class Corpus:
    # Constructeur de la classe Corpus
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.full_text = ""  # Initialise une chaîne vide pour stocker le texte complet concaténé

    def add(self, doc):
        # Ajoute un document au corpus
        if doc.auteur not in self.aut2id:                    # Vérification si l'auteur du document est déjà présent dans le corpus
            self.naut += 1                                   
            self.authors[self.naut] = Author(doc.auteur)     # Création d'un nouvel auteur et ajout au corpus
            self.aut2id[doc.auteur] = self.naut              # Ajout d'un auteur au dictionnaire
        self.authors[self.aut2id[doc.auteur]].add(doc.texte) # Incrémentation du nombre de documents produits par l'auteur

        # Ajout du document au dictionnaire id2doc
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
    
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values()) # Récupération de la liste des documents
        # Triage alphabétique des documents
        if tri == "abc":
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        # Triage temporel des documents
        elif tri == "123":
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs)))) # Affichage des documents

    def __repr__(self):
        docs = list(self.id2doc.values())                        # Récupèration de la liste des documents
        docs = list(sorted(docs, key=lambda x: x.titre.lower())) # Triage des documents par ordre alphabétique

        return "\n".join(list(map(str, docs))) # Retourne la représentation du corpus
    
    def clear(self):
        self.id2doc = {} # Réinitialisation de la liste des documents
    
    # Fonction pour concaténer l'intégralité des textes des documents
    def concat_text(self):
        texts = [doc.texte for doc in self.id2doc.values()]
        self.full_text = "\n".join(texts)

    # Fonction de recherche utilisant des expressions régulières
    def search(self, keyword):
        if not self.full_text:  # Vérifie si le texte complet a déjà été concaténé
            self.concat_text()

        # Utilisation de re.finditer pour trouver toutes les occurrences du mot-clé dans le texte complet
        matches = re.finditer(r'\b{}\b'.format(re.escape(keyword)), self.full_text, re.IGNORECASE)
        passages = [match.group(0) for match in matches]

        return passages
    
    def concorde(self, expression, context_size=20):
        if not self.full_text:
            self.concat_text()

        matches = re.finditer(expression, self.full_text, re.IGNORECASE)
        concordance_data = []

        for match in matches:
            start_idx = max(match.start() - context_size, 0)
            end_idx = min(match.end() + context_size, len(self.full_text))
            left_context = self.full_text[start_idx:match.start()].strip()
            right_context = self.full_text[match.end():end_idx].strip()
            found_text = match.group(0)

            concordance_data.append({
                'contexte gauche': left_context,
                'motif trouvé': found_text,
                'contexte droit': right_context
            })

        # Utilisation de pandas pour afficher les résultats dans un tableau
        df = pd.DataFrame(concordance_data)
        return df

class CorpusSingleton:
    _instance = None # Variable pour stocker l'instance unique de Corpus

    # Méthode spéciale pour créer une nouvelle instance si aucune n'existe encore
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)        # Création d'une nouvelle instance si elle n'existe pas déjà
            cls._instance.corpus = Corpus("Mon corpus") # Initialisation de l'instance de Corpus à l'intérieur du Singleton
        return cls._instance

    # Méthode pour récupérer l'instance de Corpus
    def get_corpus(self):
        return self.corpus # Renvoi de l'unique instance de Corpus