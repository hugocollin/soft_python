from Author import Author

import re
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

class Corpus:
    # Constructeur de la classe Corpus
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.full_text = ""

    # Méthode pour ajouter un document au corpus
    def add(self, doc):
        # Vérification si l'auteur du document est déjà présent dans le corpus
        if doc.auteur not in self.aut2id:
            self.naut += 1                               # Incrémentation du nombre d'auteurs
            self.authors[self.naut] = Author(doc.auteur) # Création d'un nouvel auteur et ajout au corpus
            self.aut2id[doc.auteur] = self.naut          # Ajout d'un auteur au dictionnaire

        self.authors[self.aut2id[doc.auteur]].add(doc.texte) # Incrémentation du nombre de documents produits par l'auteur
        self.ndoc += 1                                       # Incrémentation du nombre de documents
        self.id2doc[self.ndoc] = doc                         # Ajout du document au dictionnaire
    
    # Méthode pour afficher les résultats de la recherche
    def show(self, tri, n_docs=-1, similarites=None):
        docs = list(self.id2doc.values()) # Récupération de la liste des documents

        # Triage alphabétique des documents
        if tri == "alpha":
            docs.sort(key=lambda x: x.titre.lower())
        # Triage chronologique des documents
        elif tri == "chrono":
            docs.sort(key=lambda x: x.date, reverse=True)
        # Triage par similarité
        elif tri == "simi":
            indices = [i for i in self.id2doc.keys() if i <= len(similarites)] # Récupération des indices des documents
            indices.sort(key=lambda x: similarites[x], reverse=True)           # Triage des indices par similarité
            docs = [self.id2doc[id] for id in indices]                         # Récupération des documents triés

        # Sélection des n_docs documents les plus pertinents
        if n_docs != -1:
            docs = docs[:n_docs]

        # Retour du résultat
        return "\n".join(list(map(str, docs)))
    
    # Méthode pour réinitialiser le corpus
    def clear(self):
        self.id2doc = {}
    
    # Méthode pour concaténer le texte de tous les documents du corpus
    def concat_text(self):
        textes = [doc.texte for doc in self.id2doc.values()]
        self.full_text = "\n".join(textes)

    # Méthode pour rechercher un mot-clé dans le corpus
    def search(self, keyword):
        # Si le texte complet n'a pas encore été concaténé, on le fait
        if not self.full_text:
            self.concat_text()

        # Utilisation de re.finditer pour trouver toutes les occurrences du mot-clé dans le texte complet
        matches = re.finditer(r'\b{}\b'.format(re.escape(keyword)), self.full_text, re.IGNORECASE)
        passages = [match.group(0) for match in matches]

        return passages
    
    # Méthode pour rechercher une expression régulière dans le corpus
    def concorde(self, expression, context_size=20):
        # Si le texte complet n'a pas encore été concaténé, on le fait
        if not self.full_text:
            self.concat_text()

        # Utilisation de re.finditer pour trouver toutes les occurrences de l'expression régulière dans le texte complet
        matches = re.finditer(expression, self.full_text, re.IGNORECASE)
        concordance_data = []

        # Pour chaque occurrence, on récupère le contexte gauche et droit
        for match in matches:
            start_idx = max(match.start() - context_size, 0)               # Vérification que l'indice de début ne soit pas négatif
            end_idx = min(match.end() + context_size, len(self.full_text)) # Vérification que l'indice de fin ne dépasse pas la taille du texte
            left_context = self.full_text[start_idx:match.start()].strip() # Récupération du contexte gauche
            right_context = self.full_text[match.end():end_idx].strip()    # Récupération du contexte droit
            found_text = match.group(0)                                    # Récupération du motif trouvé

            # Ajout des résultats dans une liste
            concordance_data.append({
                'contexte gauche': left_context,
                'motif trouvé': found_text,
                'contexte droit': right_context
            })

        # Affichage des résultats dans un tableau
        df = pd.DataFrame(concordance_data)
        return df
    
    # Méthode pour nettoyer le texte d'un document
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

    # Méthode afficher les statistiques de la recherche
    def stats(self, n, temps_execution):
        # Création du vocabulaire
        vocabulaire = set() # Initialisation du vocabulaire                       
        for doc in self.id2doc.values():
            texte = self.nettoyer_texte(doc.texte) # Nettoyage du texte
            mots = texte.split()                   # Tokenisation
            vocabulaire.update(mots)               # Ajout des mots au vocabulaire

        # Comptage des occurrences
        occurrences = Counter() # Initialisation du compteur d'occurrences
        doc_freq = Counter()    # Initialisation du compteur de fréquence des documents
        for doc in self.id2doc.values():
            texte = self.nettoyer_texte(doc.texte) # Nettoyage du texte
            mots = texte.split()                   # Tokenisation
            occurrences.update(mots)               # Ajout des mots au compteur d'occurrences
            doc_freq.update(set(mots))             # Ajout des mots au compteur de fréquence des documents

        # Création du tableau de fréquences
        freq = pd.DataFrame.from_dict(occurrences, orient='index', columns=['Term Frequency'])
        freq['Document Frequency'] = pd.Series(doc_freq)

        # Affichage des statistiques de la recherche
        print("----------/ Statistiques générales de la recherche /----------\n")
        print(f"Temps d'exécution de la recherche : {temps_execution} secondes")
        print(f"Nombre de mots différents dans les documents : {len(vocabulaire)}")
        print(f"Les {n} mots les plus fréquents dans les documents :")
        print(freq.nlargest(n, 'Term Frequency'))
        print("\n----------/ Résultats de la recherche /----------")

        return freq
    
    # Méthode pour construire le vocabulaire
    def build_vocab(self):
        self.vocab = {}                                                                         
        for doc in self.id2doc.values():
            texte = self.nettoyer_texte(doc.texte) # Nettoyage du texte
            mots = texte.split()                   # Tokenisation
            for mot in mots:                                                                   
                if mot not in self.vocab:
                    self.vocab[mot] = {'id': len(self.vocab), 'occurrences': 0, 'doc_freq': 0} # Ajout d'un mot au vocabulaire
                self.vocab[mot]['occurrences'] += 1                                            # Incrémentation du nombre d'occurrences du mot

    # Méthode pour construire la matrice TF
    def build_mat_TF(self):
        rows, cols, data = [], [], []
        doc_ids = list(self.id2doc.keys()) # Récupération des identifiants des documents
        for new_doc_id, doc_id in enumerate(doc_ids):
            doc = self.id2doc[doc_id]              # Récupération du document
            texte = self.nettoyer_texte(doc.texte) # Nettoyage du texte
            mots = texte.split()                   # Tokenisation
            counts = Counter(mots)                 # Comptage des occurrences
            for mot, count in counts.items():
                if mot in self.vocab:
                    rows.append(new_doc_id)            # Ajout de l'identifiant du document
                    cols.append(self.vocab[mot]['id']) # Ajout de l'identifiant du mot
                    data.append(count)                 # Ajout du nombre d'occurrences du mot
                    self.vocab[mot]['doc_freq'] += 1   # Incrémentation de la fréquence du mot dans les documents
        
        # Création de la matrice TF
        self.mat_TF = csr_matrix((data, (rows, cols)), shape=(len(self.id2doc), len(self.vocab)))

    # Méthode pour construire la matrice TFxIDF
    def build_mat_TFxIDF(self):
        N = len(self.id2doc)                                                                   # Récupération du nombre de documents
        idf = np.log(N / np.array([self.vocab[mot]['doc_freq'] for mot in self.vocab.keys()])) # Calcul de l'IDF
        self.mat_TFxIDF = self.mat_TF.multiply(idf)                                            # Calcul de la matrice TFxIDF

    # Méthode pour vectoriser une requête
    def vectoriser_recherche(self, requete):
        mots = self.nettoyer_texte(requete).split() # Nettoyage du texte et tokenisation
        vecteur = np.zeros(len(self.vocab))         # Initialisation du vecteur de requête
        for mot in mots:
            if mot in self.vocab:
                vecteur[self.vocab[mot]['id']] += 1 # Incrémentation du nombre d'occurrences du mot dans la requête

        return vecteur

    # Méthode pour calculer les similarités entre la requête et les documents
    def calculer_similarites(self, vecteur_requete):
        produit_scalaire = self.mat_TFxIDF.dot(vecteur_requete)              # Calcul du produit scalaire entre la matrice TFxIDF et le vecteur de requête
        norme_requete = np.linalg.norm(vecteur_requete)                      # Calcul de la norme du vecteur de requête
        normes_documents = np.linalg.norm(self.mat_TFxIDF.toarray(), axis=1) # Calculer la norme de chaque vecteur de document

        # Ajout d'un epsilon pour éviter les divisions par zéro
        epsilon = 1e-10
        norme_requete += epsilon
        normes_documents += epsilon

        # Calcul des similarités
        similarites = produit_scalaire / (norme_requete * normes_documents)

        # Renvoi d'un dictionnaire contenant les identifiants des documents et leurs similarités
        return {id: sim for id, sim in zip(self.id2doc.keys(), similarites)}

class CorpusSingleton:
    _instance = None # Variable pour stocker l'instance unique de Corpus

    # Méthode spéciale pour créer une nouvelle instance si aucune n'existe encore
    def __new__(cls):
        if cls._instance is None:                       # Vérification si une instance de Corpus existe déjà
            cls._instance = super().__new__(cls)        # Création d'une nouvelle instance si elle n'existe pas déjà
            cls._instance.corpus = Corpus("Résultats")  # Initialisation de l'instance de Corpus à l'intérieur du Singleton
        return cls._instance

    # Méthode pour récupérer l'instance de Corpus
    def get_corpus(self):
        return self.corpus
    
    # Méthode pour réinitialiser l'instance de Corpus
    def reset_corpus(self):
        self.corpus = Corpus("Résultats")