class Document:
    # Constructeur de la classe Document
    def __init__(self, titre="", auteur="", date="", url="", texte="", source=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.source = source

    # Méthode pour récupérer le type du document
    def get_source(self):
        return self.source

    # Acceseur du nombre de caractères
    def get_nb_caracteres(self):
        return len(self.texte)
    
    # Acceseur du nombre de mots
    def get_nb_mots(self):
        return len(self.texte.split())
    
    # Acceseur du nombre de phrases
    def get_nb_phrases(self):
        return self.texte.count('.') + self.texte.count('!') + self.texte.count('?')
    
    # Méthode pour afficher toutes les informations d'une instance
    def __repr__(self):
        return f"\n\nTitre : {self.titre}\nAuteur : {self.auteur}\nDate : {self.date}\nURL : {self.url}\nTexte : {self.texte}\nSource : {self.source}\t"

# Classe RedditDocument héritant de Document
class RedditDocument(Document):
    # Constructeur de la classe RedditDocument
    def __init__(self, titre="", auteur="", date="", url="", texte="", nb_commentaires=0, similarite="N/A"):
        super().__init__(titre, auteur, date, url, texte, source="Reddit")
        self.nb_commentaires = nb_commentaires
        self.similarite = similarite
    
    # Renvoie le type spécifique du document Reddit
    def get_source(self):
        return "Reddit"

    # Accesseur pour le nombre de commentaires
    def get_nb_commentaires(self):
        return self.nb_commentaires

    # Mutateur pour le nombre de commentaires
    def set_nb_commentaires(self, nb_commentaires):
        self.nb_commentaires = nb_commentaires

    # Accesseur pour le taux de similarité
    def get_similarite(self):
        return self.similarite
    
    # Méthode pour afficher toutes les informations d'une instance d'un document Reddit
    def __repr__(self):
        base_repr = super().__repr__()
        pourcentage_similarite = round(self.similarite * 100, 1) if self.similarite != "N/A" else "N/A"
        return f"{base_repr}\nNombre de commentaires : {self.nb_commentaires}\nStatistiques du document :\n   Pertinence : {pourcentage_similarite}%\n   Nombre de caractères : {self.get_nb_caracteres()}\n   Nombre de mots : {self.get_nb_mots()}\n   Nombre de phrases : {self.get_nb_phrases()}\t"

# Classe ArxivDocument héritant de Document
class ArxivDocument(Document):
    # Constructeur de la classe ArxivDocument
    def __init__(self, titre="", auteurs="", date="", url="", texte="", similarite="N/A"):
        super().__init__(titre, "", date, url, texte, source="Arxiv")
        self.auteurs = auteurs
        self.similarite = similarite

    # Accesseur pour la liste des co-auteurs
    def get_auteurs(self):
        return self.auteurs

    # Méthode pour ajouter un co-auteur
    def ajouter_auteur(self, auteur):
        self.auteurs.append(auteur)

    # Renvoie le type spécifique du document Arxiv
    def get_source(self):
        return "Arxiv"

    # Accesseur pour le taux de similarité
    def get_similarite(self):
        return self.similarite

    # Méthode pour afficher toutes les informations d'une instance d'un document Arxiv
    def __repr__(self):
        auteur_principal = self.auteurs[0] if self.auteurs else "Aucun"
        co_auteurs = ", ".join(self.auteurs[1:]) if len(self.auteurs) > 1 else "Aucun"
        pourcentage_similarite = round(self.similarite * 100, 1) if self.similarite != "N/A" else "N/A"
        return f"\n\nTitre : {self.titre}\nAuteur : {auteur_principal}\nCo-auteurs : {co_auteurs}\nDate : {self.date}\nURL : {self.url}\nTexte : {self.texte}\nSource : {self.source}\nStatistiques du document :\n   Pertinence : {pourcentage_similarite}%\n   Nombre de caractères : {self.get_nb_caracteres()}\n   Nombre de mots : {self.get_nb_mots()}\n   Nombre de phrases : {self.get_nb_phrases()}\t"

    # [DEBUG]
    def __str__(self):
        liste_auteurs = ", ".join(self.auteurs)
        return f"{super().__str__()}, Auteurs : {liste_auteurs}"

# Classe DocumentFactory
class DocumentFactory:
    @staticmethod
    def create_document(doc_source, *args, **kwargs):
        if doc_source == "reddit":                    # Création d'une instance de RedditDocument avec les arguments spécifiés
            return RedditDocument(*args, **kwargs)
        elif doc_source == "arxiv":                   # Création d'une instance de ArxivDocument avec les arguments spécifiés
            return ArxivDocument(*args, **kwargs)
        else:                                         # Si le type n'est pas reconnu, création d'une instance de Document par défaut
            return Document(*args, **kwargs)