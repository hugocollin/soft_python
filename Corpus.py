from Document import RedditDocument, ArxivDocument
from Author import Author

class Corpus:
    # Constructeur de la classe Corpus
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

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