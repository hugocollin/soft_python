from Document import RedditDocument, ArxivDocument
from Author import Author
from Corpus import CorpusSingleton

import praw
import urllib.request
import xmltodict
import time
import datetime
import pickle

# Fonction principale du moteur de recherche
def recherche(topic, mots_cles, nombre_articles, methode_affichage):
    # Initilisation de variables globales
    debut_recherche = time.time()                  # Enregistrement du temps de début de traitement
    topic_str = str(topic)                         # Conversion de la variable en chaine de caractères
    nombre_articles_int = int(nombre_articles)     # Conversion de la variable en entier
    methode_affichage_str = str(methode_affichage) # Conversion de la variable en chaine de caractères

    # Initialisation des listes de textes par source
    textes_reddit = []       # Initialisation de la liste de textes Reddit
    textes_arxiv = []        # Initialisation de la liste de textes ArXiv
    textes_bruts_reddit = [] # Initialisation de la liste de textes bruts Reddit
    textes_bruts_arxiv = []  # Initialisation de la liste de textes bruts ArXiv

    # Paramètres de recherche de Reddit
    reddit = praw.Reddit(client_id='-GD1SJ96QztEIjktZ0o6nQ', client_secret='GinKmTjo2ggKztu0bwSb6mlXHX57Pw', user_agent='FAC', check_for_async=False) # Connexion à Reddit en utilisant les identifiants
    subr = reddit.subreddit(topic_str).hot(limit=nombre_articles_int)                                                                                 # Recherche des documents correspondants au topic de la recherche

    # Vérification si le nombre d'articles trouvés est suffisant
    if subr:
        # Récupération des posts Reddit
        for post in subr:
            texte = post.title                           # Extraction du contenu textuel
            texte = texte.replace("\n", " ")             # Remplacement des retours à la ligne par des espaces dans le titre
            textes_reddit.append(texte)                  # Ajout du texte à la liste de textes
            textes_bruts_reddit.append(("Reddit", post)) # Ajout du texte brut à la liste de textes bruts
    else:
        print("[WARNING] : Aucun document trouvé sur Reddit")

    # Paramètres de recherche de Arxiv
    url = 'http://export.arxiv.org/api/query?search_query=all:' + topic_str + '&start=0&max_results=' + str(nombre_articles_int) # Recherche des documents correspondants au topic de la recherche
    data = urllib.request.urlopen(url)                                                                                           # Ouverture de la connexion HTTP
    data = xmltodict.parse(data.read().decode('utf-8'))                                                                          # Décodage et analyse des données au format XML

    # Vérification si le nombre d'articles trouvés est suffisant
    if 'entry' in data['feed'] and data['feed']['entry']:
        # Récupération des posts Arxiv
        for document in data['feed']['entry']:
            texte = document['title']+ ". " + document['summary'] # Extraction du contenu textuel
            texte = texte.replace("\n", " ")                      # Remplacement des retours à la ligne par des espaces dans le titre
            textes_arxiv.append(texte)                            # Ajout du texte à la liste de textes
            textes_bruts_arxiv.append(("ArXiv", document))        # Ajout du texte brut à la liste de textes bruts
    else:
        print("[WARNING] : Aucun document trouvé sur ArXiv")

    # Suppression des textes trop courts
    textes_reddit = [texte for texte in textes_reddit if len(texte) >= 100]
    textes_arxiv = [texte for texte in textes_arxiv if len(texte) >= 100]

    # Initialisation des listes de textes
    textes = []       # Initialisation de la liste de textes
    textes_bruts = [] # Initialisation de la liste de textes bruts
    index_reddit = 0  # Initialisation de l'index de parcour sur les textes Reddit
    index_arxiv = 0   # Initialisation de l'index de parcour sur les textes ArXiv

    # Ajout du nombre de documents nécessaires à la liste de textes
    # Arrêt si on a atteint le nombre de documents demandés ou si on a parcouru tous les documents
    while len(textes) < nombre_articles_int and (index_reddit < len(textes_reddit) or index_arxiv < len(textes_arxiv)):
        # Vériication qu'il y ait encore des textes Reddit
        if index_reddit < len(textes_reddit):
            textes.append(textes_reddit[index_reddit])
            textes_bruts.append(textes_bruts_reddit[index_reddit])
            index_reddit += 1
        # Vériication qu'il y ait encore des textes ArXiv
        if index_arxiv < len(textes_arxiv):
            textes.append(textes_arxiv[index_arxiv])
            textes_bruts.append(textes_bruts_arxiv[index_arxiv])
            index_arxiv += 1

    textes = " ".join(textes) # Concaténation des textes en une seule chaîne de caractères

    collection = [] # Initialisation d'une liste vide pour contenir tout les documents de la recherche

    # Création des documents à partir des données brutes
    for nature, texte in textes_bruts:
        # Si la nature du document est "Reddit"
        if nature == "Reddit":
            titre = texte.title.replace("\n", '')                                       # Remplacement des retours à la ligne par des espaces dans le titre
            auteur = str(texte.author)                                                  # Convertion de l'auteur en chaîne de caractères
            date = datetime.datetime.fromtimestamp(texte.created).strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour
            url = "https://www.reddit.com/"+ texte.permalink                            # Création de l'URL du texte
            nb_commentaires = texte.num_comments                                        # Récupération du nombre de commentaires
            texte = texte.selftext.replace("\n", "")                                    # Remplacement des retours à la ligne par des espaces dans le texte
            document = RedditDocument(titre, auteur, date, url, texte, nb_commentaires) # Création d'un document à partir des données récupérées
            collection.append(document)                                                 # Ajout du document à la liste collection

        # Sinon, si la nature du document est "ArXiv"
        elif nature == "ArXiv": 
            titre = texte["title"].replace('\n', '')                                                         # Remplacement des retours à la ligne par des espaces dans le titre
            raw_authors = texte.get("author", [])                                                            # Récupération des auteurs
            if isinstance(raw_authors, dict):                                                                # Si les données brutes de l'auteur sont un dictionnaire
                auteurs = [raw_authors.get("name", "")]
            else:                                                                                            # Si les données brutes de l'auteur sont une liste de dictionnaires
                auteurs = [a.get("name", "") for a in raw_authors if isinstance(a, dict)]
            summary = texte["summary"].replace("\n", "")                                                     # Remplacement des retours à la ligne par des espaces dans le texte
            date = datetime.datetime.strptime(texte["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d") # Formatage de la date en année/mois/jour
            document = ArxivDocument(titre, auteurs, date, texte["id"], summary)                             # Création d'un document à partir des données récupérées
            collection.append(document)                                                                      # Ajout du document à la liste collection

    # Création de l'index de documents
    id2doc = {}
    for i, doc in enumerate(collection):
        id2doc[i] = doc.titre

    # Initialisation des dictionnaires de stockage des auteurs
    auteurs = {}        # Initialisation d'un dictionnaire vide pour contenir les auteurs
    aut2id = {}         # Initialisation d'un dictionnaire vide pour contenir les index des auteurs
    nombre_auteurs = 0  # Initialisation du nombre d'auteurs

    # Création de la liste et index des auteurs
    for texte in collection:
        if texte.auteur not in aut2id:                     # Si l'auteur n'est pas dans le dictionnaire des index des auteurs
            nombre_auteurs += 1                            # Incrémentation du nombre d'auteurs
            auteurs[nombre_auteurs] = Author(texte.auteur) # Ajout de l'auteur à la liste des auteurs
            aut2id[doc.auteur] = nombre_auteurs            # Ajout de l'index de l'auteur au dictionnaire des index des auteurs

        auteurs[aut2id[doc.auteur]].add(texte.texte) # Ajout du texte à la production de l'auteur

    # Initialisation de l'unique Corpus
    corpus_singleton = CorpusSingleton()   # Initialisation du singleton
    corpus_singleton.reset_corpus()        # Initialisation du corpus
    corpus = corpus_singleton.get_corpus() # Récupération du corpus

    # Vidage du corpus puis remplissage
    corpus.clear()
    for doc in collection:
        corpus.add(doc)

    # Traitement sur le corpus
    corpus.build_vocab()                                       # Construction du vocabulaire
    corpus.build_mat_TF()                                      # Construction de la matrice TF
    corpus.build_mat_TFxIDF()                                  # Construction de la matrice TFxIDF
    
    vecteur_requete = corpus.vectoriser_recherche(mots_cles)   # Vectorisation de la requête
    
    similarites = corpus.calculer_similarites(vecteur_requete) # Calcul des similarités
    # Mise à jour de la similarité de chaque document
    for id, sim in similarites.items():
        corpus.id2doc[id].similarite = sim

    # Enregistrement du corpus (traitement à revoir)
    # Ouverture d'un fichier, puis écriture avec pickle
    with open("corpus.pkl", "wb") as f:
        pickle.dump(corpus, f)

    # Supression de la variable corpus
    del corpus

    # Ouverture du fichier, puis lecture avec pickle
    with open("corpus.pkl", "rb") as f:
        corpus = pickle.load(f)

    # Traitement sur l'affichage des statistiques de la recherche
    fin_recherche = time.time()                                 # Enregistrement du temps de fin de traitement
    temps_execution = round(fin_recherche - debut_recherche, 2) # Calcul du temps d'exécution
    corpus.stats(10, temps_execution)                           # Affichage des statistiques du corpus

    # Traitement sur l'affichage des documents de la recherche
    if methode_affichage_str == "Pertinence":
        methode_affichage_str = "simi"
    elif methode_affichage_str == "Temporelle":
        methode_affichage_str = "chrono"
    elif methode_affichage_str == "Alphabétique":
        methode_affichage_str = "alpha"
    return corpus.show(tri=methode_affichage_str, similarites=similarites)