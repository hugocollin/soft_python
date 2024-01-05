class Document:
    # Constructeur de la classe Document
    def __init__(self, titre="", auteur="", date="", url="", texte="", type=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type
    
    # Méthode pour afficher toutes les informations d'une instance
    def __repr__(self):
        return f"\n\nTitre : {self.titre}\nAuteur : {self.auteur}\nDate : {self.date}\nURL : {self.url}\nTexte : {self.texte}\nType : {self.type}\t"

    # Méthode de représentation de la classe Document
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    
    # Méthode pour récupérer le type du document
    def getType(self):
        return self.type

# Classe RedditDocument héritant de Document
class RedditDocument(Document):
    # Constructeur de la classe RedditDocument
    def __init__(self, titre="", auteur="", date="", url="", texte="", nb_commentaires=0):
        super().__init__(titre, auteur, date, url, texte, type="Reddit")
        self.nb_commentaires = nb_commentaires

    # Accesseur pour le nombre de commentaires
    def get_nb_commentaires(self):
        return self.nb_commentaires

    # Mutateur pour le nombre de commentaires
    def set_nb_commentaires(self, nb_commentaires):
        self.nb_commentaires = nb_commentaires

    # Méthode d'affichage spécifique pour RedditDocument
    def __str__(self):
        return f"{super().__str__()}, {self.nb_commentaires} commentaires"
    
    # Renvoie le type spécifique du document Reddit
    def getType(self):
        return "Reddit"

# Classe ArxivDocument héritant de Document
class ArxivDocument(Document):
    # Constructeur de la classe ArxivDocument
    def __init__(self, titre="", auteurs=None, date="", url="", texte=""):
        super().__init__(titre, "", date, url, texte, type="Arxiv")
        if auteurs is None:
            self.auteurs = []
        else:
            self.auteurs = auteurs

    # Accesseur pour la liste des co-auteurs
    def get_auteurs(self):
        return self.auteurs

    # Méthode pour ajouter un co-auteur
    def ajouter_auteur(self, auteur):
        self.auteurs.append(auteur)

    # Méthode d'affichage spécifique pour ArxivDocument
    def __str__(self):
        liste_auteurs = ", ".join(self.auteurs)
        return f"{super().__str__()}, Co-auteurs : {liste_auteurs}"
    
    # Renvoie le type spécifique du document Arxiv
    def getType(self):
        return "Arxiv"

# Classe DocumentFactory
class DocumentFactory:
    @staticmethod
    def create_document(doc_type, *args, **kwargs):
        if doc_type == "reddit":                    # Création d'une instance de RedditDocument avec les arguments spécifiés
            return RedditDocument(*args, **kwargs)
        elif doc_type == "arxiv":                   # Création d'une instance de ArxivDocument avec les arguments spécifiés
            return ArxivDocument(*args, **kwargs)
        else:                                       # Si le type n'est pas reconnu, création d'une instance de Document par défaut
            return Document(*args, **kwargs)