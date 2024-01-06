from Author import Author             # Importation de la classe Author depuis le module Author

import re                             # Importation de la bibliotheque re, afin de travailler avec des expressions régulières
import pandas as pd                   # Importation de la bibliotheque pandas, afin de manipuler et d'analyser des données
import numpy as np                    # Importation de la bibliotheque numpy, afin de manipuler des matrices
import nltk                           # Importation de la bibliotheque nltk, afin de traiter des données textuelles
from nltk.corpus import stopwords     # Importation de la bibliotheque stopwords, afin de supprimer les mots vides
from nltk.stem import SnowballStemmer # Importation de la bibliotheque SnowballStemmer, afin de raciniser les mots
from scipy.sparse import csr_matrix   # Importation de la bibliotheque csr_matrix, afin de créer une matrice creuse
from collections import Counter       # Importation de la bibliotheque Counter, afin de compter les occurrences

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
    
    @staticmethod
    def nettoyer_texte(texte):
        texte = texte.lower()                                                  # Conversion du texte en minuscules
        texte = texte.replace('\n', ' ')                                       # Remplacement des passages à la ligne par des espaces
        tokens = texte.split()                                                 # Tokenisation
        tokens = [token for token in tokens if not re.match(r"[,.!?]", token)] # Suppression de la ponctuation
        tokens = [token for token in tokens if token.isalnum()]                # Suppression des caractères qui ne sont pas alphanumériques
        stop_words = set(stopwords.words("english"))                           # Récupération des stop words anglais
        tokens = [token for token in tokens if token not in stop_words]        # Suppression des stop words anglais
        tokens = [token for token in tokens if len(token) > 1]                 # Suppression des token contenant un seul caractère
        stemmer = SnowballStemmer("english")                                   # Initialisation du stemmer anglais
        tokens = [stemmer.stem(token) for token in tokens]                     # Racinisation des tokens
        return " ".join(tokens)

    def stats(self, n):
        # Construction du vocabulaire
        vocabulaire = set()
        for doc in self.id2doc.values():
            texte = self.nettoyer_texte(doc.texte)
            mots = texte.split()
            vocabulaire.update(mots)

        # Comptage des occurrences
        occurrences = Counter()
        doc_freq = Counter()
        for doc in self.id2doc.values():
            texte = self.nettoyer_texte(doc.texte)
            mots = texte.split()
            occurrences.update(mots)
            doc_freq.update(set(mots))

        # Création du tableau de fréquences
        freq = pd.DataFrame.from_dict(occurrences, orient='index', columns=['Term Frequency'])
        freq['Document Frequency'] = pd.Series(doc_freq)

        # Affichage des statistiques
        print(f"Nombre de mots différents dans le corpus : {len(vocabulaire)}")
        print(f"Les {n} mots les plus fréquents dans le corpus :")
        print(freq.nlargest(n, 'Term Frequency'))

        return freq
    
    def build_vocab(self):
        self.vocab = {}
        for doc in self.id2doc.values():
            texte = self.nettoyer_texte(doc.texte)
            mots = texte.split()
            for mot in mots:
                if mot not in self.vocab:
                    self.vocab[mot] = {'id': len(self.vocab), 'occurrences': 0, 'doc_freq': 0}
                self.vocab[mot]['occurrences'] += 1

    def build_mat_TF(self):
        rows, cols, data = [], [], []
        doc_ids = list(self.id2doc.keys())
        for new_doc_id, doc_id in enumerate(doc_ids):
            doc = self.id2doc[doc_id]
            texte = self.nettoyer_texte(doc.texte)
            mots = texte.split()
            counts = Counter(mots)
            for mot, count in counts.items():
                if mot in self.vocab:
                    rows.append(new_doc_id)
                    cols.append(self.vocab[mot]['id'])
                    data.append(count)
                    self.vocab[mot]['doc_freq'] += 1
        self.mat_TF = csr_matrix((data, (rows, cols)), shape=(len(self.id2doc), len(self.vocab)))

    def build_mat_TFxIDF(self):
        N = len(self.id2doc)
        idf = np.log(N / np.array([self.vocab[mot]['doc_freq'] for mot in self.vocab.keys()]))
        self.mat_TFxIDF = self.mat_TF.multiply(idf)                                            

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