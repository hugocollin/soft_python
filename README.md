# Moteur de recherche Python

## Installation

1. Clonez ce dépôt sur votre machine locale.
2. Assurez-vous d'avoir un noyau Python installé avec les bibliothèques suivantes :
    - ipywidgets
    - IPython.display
    - praw
    - urllib.request
    - xmltodict
    - time
    - datetime
    - pickle
    - re
    - pandas
    - numpy
    - nltk
    - scipy
    - sklearn
    - collections

    - pytest*
    - warnings*

**Ces bibliothèques ne sont pas nécessaires au fonctionnement de l'application, celles-ci sont seulement utiles pour tester le code de l'application.*

## Utilisation

1. Exécutez la seule cellule du fichier 'Interface.ipynb' avec votre noyau Python contenant les bibliothèques précédemment installées pour démarrer le moteur de recherche.
2. L'interface du moteur de recherche apparaît en bas de la cellule exécutée. Vous pourrez alors rentrer les paramètres de la recherche :
    - Topic : permet de renseigner le sujet global de la recherche souhaitée. Attention, celui-ci ne doit être constitué que d'un seul mot.
    - Mots clés : permet de renseigner des mots qui viendront compléter et affiner le sujet global de la recherche afin d'obtenir des résultats plus pertinents.
    - Nombre d'articles à extraire : permet de sélectionner le nombre d'articles à extraire (de 1 à 1000). Si vous saisissez le nombre d'articles à extraire via votre clavier, cliquez sur la touche [ENTRÉE] pour confirmer la saisie. Attention, ce paramètre fait varier le temps d'exécution de la recherche (comptez environ 30 secondes pour une recherche de 1000 articles).
    - Méthode d'affichage : permet de sélectionner une option parmi les 3 proposées :
        - Pertinence : classe les résultats de manière décroissante selon leur score de pertinence.
        - Temporelle : classe les résultats de manière décroissante selon leur date de publication.
        - Alphabétique : classe les résultats de manière croissante selon la première lettre de leur titre.
3. Cliquez ensuite sur le bouton "Rechercher" pour lancer la recherche selon les paramètres précédemment renseignés. Attention, l'affichage des résultats n'est pas instantané, dès que ceux-ci seront prêts, ils s'afficheront en dessous du moteur de recherche. Vous y retrouverez les statistiques générales de la recherche ainsi que tous les résultats de la recherche en détail.