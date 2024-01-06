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


    textes_reddit = [] # Initialisation de la liste de textes Reddit
    textes_arxiv = []  # Initialisation de la liste de textes ArXiv

    textes_bruts_reddit = [] # Initialisation de la liste de textes bruts Reddit
    textes_bruts_arxiv = []  # Initialisation de la liste de textes bruts ArXiv


    # Paramètres de recherche de Reddit
    reddit = praw.Reddit(client_id='-GD1SJ96QztEIjktZ0o6nQ', client_secret='GinKmTjo2ggKztu0bwSb6mlXHX57Pw', user_agent='FAC') # Connexion à Reddit en utilisant les identifiants
    subr = reddit.subreddit(recherche_str).hot(limit=nombre_articles_int)                                                      # Recherche des documents correspondants au topic de la recherche

    if subr:
        # Récupération des posts Reddit
        for post in subr:
            texte = post.title                           # Extraction du contenu textuel
            texte = texte.replace("\n", " ")             # Remplacement des retours à la ligne par des espaces dans le titre
            textes_reddit.append(texte)                  # Ajout du texte à la liste de textes
            textes_bruts_reddit.append(("Reddit", post)) # Ajout du texte brut à la liste de textes bruts
    else:
        print("Aucun document trouvé sur Reddit")


    # Paramètres de recherche de Arxiv
    url = 'http://export.arxiv.org/api/query?search_query=all:' + recherche_str + '&start=0&max_results=' + str(nombre_articles_int) # Recherche des documents correspondants au topic de la recherche
    data = urllib.request.urlopen(url)                                                                                               # Ouverture de la connexion HTTP
    data = xmltodict.parse(data.read().decode('utf-8'))                                                                              # Décode et analyse les données au format XML

    # verifier si le nombre d'articles trouvés est suffisant
    if 'entry' in data['feed'] and data['feed']['entry']:
        # Récupération des posts Arxiv
        for document in data['feed']['entry']:
            texte = document['title']+ ". " + document['summary'] # Extraction du contenu textuel
            texte = texte.replace("\n", " ")                      # Remplacement des retours à la ligne par des espaces dans le titre
            textes_arxiv.append(texte)                            # Ajout du texte à la liste de textes
            textes_bruts_arxiv.append(("ArXiv", document))        # Ajout du texte brut à la liste de textes bruts
    else:
        print("Aucun document trouvé sur ArXiv")

    # Suppression des textes trop courts
    textes_reddit = [texte for texte in textes_reddit if len(texte) >= 100]
    textes_arxiv = [texte for texte in textes_arxiv if len(texte) >= 100]

    textes = []       # Initialisation de la liste de textes
    textes_bruts = [] # Initialisation de la liste de textes bruts

    index_reddit = 0 # Initialisation de l'index de parcour sur les textes Reddit
    index_arxiv = 0  # Initialisation de l'index de parcour sur les textes ArXiv

    # On ajoute le nombre d'elements necessaires a la liste de textes
    # On s'arrete si on a parcouru tous les textes Reddit et ArXiv ou si on a atteint le nombre d'articles demandes
    while len(textes) < nombre_articles_int and (index_reddit < len(textes_reddit) or index_arxiv < len(textes_arxiv)):
        # On verifie qu'il y ait encore des textes Reddit
        if index_reddit < len(textes_reddit):
            textes.append(textes_reddit[index_reddit])
            textes_bruts.append(textes_bruts_reddit[index_reddit])
            index_reddit += 1
        # On verifie qu'il y ait encore des textes ArXiv
        if index_arxiv < len(textes_arxiv):
            textes.append(textes_arxiv[index_arxiv])
            textes_bruts.append(textes_bruts_arxiv[index_arxiv])
            index_arxiv += 1

    # Traitements sur les textes
    for i, texte in enumerate(textes): # Affichage des caractéristiques de chaque texte
        print(f"Document {i} :\t# Nombre de caractères : {len(texte)}\t# Nombre de mots : {len(texte.split(' '))}\t# Nombre de phrases : {len(texte.split('.'))}")


    textes = " ".join(textes) # Combination des éléments de la liste textes en une chaîne de caractères, en les séparant par des espaces

    collection = [] # Initialisation d'une liste vide pour contenir les documents

    for nature, texte in textes_bruts:
        # Si la nature du document est "Reddit"
        if nature == "Reddit":
            titre = texte.title.replace("\n", '')                                       # Remplacement des retours à la ligne par des espaces dans le titre
            auteur = str(texte.author)                                                  # Convertion de l'auteur en chaîne de caractères
            date = datetime.datetime.fromtimestamp(texte.created).strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour
            url = "https://www.reddit.com/"+ texte.permalink                            # Création de l'URL du texte
            texte = texte.selftext.replace("\n", "")                                    # Remplace des retours à la ligne par des espaces dans le texte
            post.comments.replace_more(limit=None)                                      # Chargement de tous les commentaires du post
            nb_commentaires = len(post.comments.list())                                 # Obtention du nombre total de commentaires
            document = RedditDocument(titre, auteur, date, url, texte, nb_commentaires) # Création d'un document à partir des données récupérées
            # print(document)                                                             # [DEBUG]
            collection.append(document)                                                 # Ajout du document à la liste collection

        # Sinon, si la nature du document est "ArXiv"
        elif nature == "ArXiv": 
            titre = texte["title"].replace('\n', '')                                                         # Remplacement des retours à la ligne par des espaces dans le titre
            try:
                auteurs = ([a.get("name", "") for a in texte.get("author", []) if isinstance(a, dict)])      # Création d'une liste d'auteurs
            except:
                auteurs = texte.get("author", {}).get("name", "")                                            # Si l'auteur est seul, il n'y a pas besoin de liste
            summary = texte["summary"].replace("\n", "")                                                     # Remplace des retours à la ligne par des espaces dans le texte
            date = datetime.datetime.strptime(texte["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d") # Formatage de la date en année/mois/jour
            document = ArxivDocument(titre, auteurs, date, texte["id"], summary)                             # Création d'un document à partir des données récupérées
            # print(document)                                                                                  # [DEBUG]
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

    # Vidage du corpus puis remplissage
    corpus.clear()
    for doc in collection:
        corpus.add(doc)

    # Construction du vocabulaire et des matrices TF et TFxIDF
    corpus.build_vocab()
    corpus.build_mat_TF()
    corpus.build_mat_TFxIDF()

    # Affichage des statistiques du corpus
    corpus.stats(10)

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