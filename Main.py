from Document import RedditDocument, ArxivDocument # Importation de la classe RedditDocument et ArxivDocument depuis le module Document
from Author import Author                          # Importation de la classe Author depuis le module Author
from Corpus import CorpusSingleton                 # Importation de la classe Corpus depuis le module Corpus

import praw           # Importation la bibliothèque praw pour accéder à l'API de Reddit
import urllib.request # Importation la bibliothèque urllib pour effectuer des requêtes HTTP 
import xmltodict      # Importation de la bibliothèque xmltodict pour analyser des données XML
import datetime       # Importation de la bibliothèque datetime pour manipuler des dates et des heures
import pickle         # Importation de la bibliothèque pickle pour convertir un objet en un format binaire pouvant être enregistré dans un fichier ou transmis sur un réseau

def recherche(recherche, nombre_articles):
    # Initilisation de variables globales
    recherche_str = str(recherche)             # Conversion de la variable en chaine de caractères
    nombre_articles_int = int(nombre_articles) # Conversion de la variable en entier
    textes = []                                # Initialisation de la liste de textes
    textes_bruts = []                          # Initialisation de la liste de textes bruts

    # Paramètres de recherche de Reddit
    reddit = praw.Reddit(client_id='-GD1SJ96QztEIjktZ0o6nQ', client_secret='GinKmTjo2ggKztu0bwSb6mlXHX57Pw', user_agent='FAC') # Connexion à Reddit en utilisant les identifiants
    subr = reddit.subreddit(recherche_str).hot(limit=nombre_articles_int)                                                      # Recherche des documents correspondants au topic de la recherche

    # Récupération des posts Reddit
    for post in subr:
        texte = post.title                    # Extraction du contenu textuel
        texte = texte.replace("\n", " ")      # Remplacement des retours à la ligne par des espaces dans le titre
        textes.append(texte)                  # Ajout du texte à la liste de textes
        textes_bruts.append(("Reddit", post)) # Ajout du texte brut à la liste de textes bruts

    # Paramètres de recherche de Arxiv
    url = 'http://export.arxiv.org/api/query?search_query=all:' + recherche_str + '&start=0&max_results=' + str(nombre_articles_int) # Recherche des documents correspondants au topic de la recherche
    data = urllib.request.urlopen(url)                                                                                               # Ouverture de la connexion HTTP
    data = xmltodict.parse(data.read().decode('utf-8'))                                                                              # Décode et analyse les données au format XML

    # Récupération des posts Arxiv
    for document in data['feed']['entry']:
        texte = document['title']+ ". " + document['summary'] # Extraction du contenu textuel
        texte = texte.replace("\n", " ")                      # Remplacement des retours à la ligne par des espaces dans le titre
        textes.append(texte)                                  # Ajout du texte à la liste de textes
        textes_bruts.append(("ArXiv", document))              # Ajout du texte brut à la liste de textes bruts

    # Traitements sur les textes
    for i, texte in enumerate(textes): # Affichage des caractéristiques de chaque texte
        print(f"Document {i} :\t# Nombre de caractères : {len(texte)}\t# Nombre de mots : {len(texte.split(' '))}\t# Nombre de phrases : {len(texte.split('.'))}")
        if len(texte)<100: # Suppression des textes comportant moins de 100 caractères
            textes.remove(texte)

    textes = " ".join(textes) # Combination des éléments de la liste textes en une chaîne de caractères, en les séparant par des espaces

    collection = [] # Initialisation d'une liste vide pour contenir les documents

    for nature, texte in textes_bruts:
        # Si la nature du document est "Reddit"
        if nature == "Reddit":
            titre = texte.title.replace("\n", '')                                      # Remplacement des retours à la ligne par des espaces dans le titre
            auteur = str(texte.author)                                                 # Convertion de l'auteur en chaîne de caractères
            date = datetime.datetime.fromtimestamp(texte.created).strftime("%Y/%m/%d") # Formatage de la date en année/mois/jour
            url = "https://www.reddit.com/"+ texte.permalink                           # Création de l'URL du texte
            texte = texte.selftext.replace("\n", "")                                   # Remplace des retours à la ligne par des espaces dans le texte
            document = RedditDocument(titre, auteur, date, url, texte)                 # Création d'un document à partir des données récupérées
            collection.append(document)                                                # Ajout du document à la liste collection

        # Sinon, si la nature du document est "ArXiv"
        elif nature == "ArXiv": 
            titre = texte["title"].replace('\n', '')                                                         # Remplacement des retours à la ligne par des espaces dans le titre
            try:
                auteurs = ", ".join([a["name"] for a in texte["author"]])                                    # Création d'une liste d'auteurs (séparés par une virgule)
            except:
                auteurs = texte["author"]["name"]                                                            # Si l'auteur est seul, il n'y a pas besoin de liste
            summary = texte["summary"].replace("\n", "")                                                     # Remplace des retours à la ligne par des espaces dans le texte
            date = datetime.datetime.strptime(texte["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d") # Formatage de la date en année/mois/jour
            document = ArxivDocument(titre, auteurs, date, texte["id"], summary)                             # Création d'un document à partir des données récupérées
            collection.append(document)                                                                      # Ajout du document à la liste collection

    # Création de l'index de documents
    id2doc = {}
    for i, doc in enumerate(collection):
        id2doc[i] = doc.titre

    auteurs = {}
    aut2id = {} 
    nombre_auteurs = 0

    # Création de la liste+index des Auteurs
    for texte in collection:
        if texte.auteur not in aut2id:
            nombre_auteurs += 1
            auteurs[nombre_auteurs] = Author(texte.auteur)
            aut2id[doc.auteur] = nombre_auteurs

        auteurs[aut2id[doc.auteur]].add(texte.texte)

    # Utilisation du Singleton pour obtenir l'instance unique de Corpus
    corpus_singleton = CorpusSingleton()
    corpus = corpus_singleton.get_corpus()

    # Nettoyage du corpus puis remplissage
    corpus.clear()
    for doc in collection:
        corpus.add(doc)

    # Ouverture d'un fichier, puis écriture avec pickle
    with open("corpus.pkl", "wb") as f:
        pickle.dump(corpus, f)

    # Supression de la variable corpus
    del corpus

    # Ouverture du fichier, puis lecture avec pickle
    with open("corpus.pkl", "rb") as f:
        corpus = pickle.load(f)

    # Affichage du corpus
    corpus.show()