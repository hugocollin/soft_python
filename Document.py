class Document:
    # Constructeur de la classe Document
    def __init__(self, titre="", auteur="", date="", url="", texte="", source=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.source = source

    # Méthode pour récupérer la source du document
    def get_source(self):
        return self.source

    # Méthode pour récupérer le nombre de caractères du document
    def get_nb_caracteres(self):
        return len(self.texte)
    
    # Méthode pour récupérer le nombre de mots du document
    def get_nb_mots(self):
        return len(self.texte.split())
    
    # Méthode pour récupérer le nombre de phrases du document
    def get_nb_phrases(self):
        return self.texte.count('.') + self.texte.count('!') + self.texte.count('?')

class RedditDocument(Document):
    # Constructeur de la classe RedditDocument
    def __init__(self, titre="", auteur="", date="", url="", texte="", nb_commentaires=0, similarite="N/A"):
        super().__init__(titre, auteur, date, url, texte, source="Reddit")
        self.nb_commentaires = nb_commentaires
        self.similarite = similarite
    
    # Méthode pour récupérer la source du document
    def get_source(self):
        return "Reddit"

    # Méthode pour récupérer le nombre de commentaires du document
    def get_nb_commentaires(self):
        return self.nb_commentaires

    # Méthode pour récupérer le taux de similarité du document
    def get_similarite(self):
        return self.similarite
    
    # Méthode pour afficher toutes les informations d'un document Reddit
    def __repr__(self):
        texte = self.texte if self.texte else "Aucun"
        pourcentage_similarite = round(self.similarite * 100, 1) if self.similarite != "N/A" else "N/A"
        return f"\n\nTitre : {self.titre}\nAuteur : {self.auteur}\nDate : {self.date}\nTexte : {texte}\nSource : {self.source}\nURL : {self.url}\nNombre de commentaires : {self.nb_commentaires}\nStatistiques du document :\n   Pertinence : {pourcentage_similarite}%\n   Nombre de caractères : {self.get_nb_caracteres()}\n   Nombre de mots : {self.get_nb_mots()}\n   Nombre de phrases : {self.get_nb_phrases()}\t"

class ArxivDocument(Document):
    # Constructeur de la classe ArxivDocument
    def __init__(self, titre="", auteurs="", date="", url="", texte="", similarite="N/A"):
        super().__init__(titre, "", date, url, texte, source="Arxiv")
        self.auteurs = auteurs
        self.similarite = similarite

    # Méthode pour récupérer la liste des auteurs
    def get_auteurs(self):
        return self.auteurs

    # Méthode pour ajouter un auteur à la liste des auteurs
    def ajouter_auteur(self, auteur):
        self.auteurs.append(auteur)

    # Méthode pour récupérer la source du document
    def get_source(self):
        return "Arxiv"

    # Méthode pour récupérer le taux de similarité du document
    def get_similarite(self):
        return self.similarite

    # Méthode pour afficher toutes les informations d'un document Arxiv
    def __repr__(self):
        auteur_principal = self.auteurs[0] if self.auteurs else "Aucun"
        co_auteurs = ", ".join(self.auteurs[1:]) if len(self.auteurs) > 1 else "Aucun"
        pourcentage_similarite = round(self.similarite * 100, 1) if self.similarite != "N/A" else "N/A"
        return f"\n\nTitre : {self.titre}\nAuteur : {auteur_principal}\nCo-auteurs : {co_auteurs}\nDate : {self.date}\nTexte : {self.texte}\nSource : {self.source}\nURL : {self.url}\nStatistiques du document :\n   Pertinence : {pourcentage_similarite}%\n   Nombre de caractères : {self.get_nb_caracteres()}\n   Nombre de mots : {self.get_nb_mots()}\n   Nombre de phrases : {self.get_nb_phrases()}\t"

class DocumentFactory:
    @staticmethod
    # Méthode pour créer un document en fonction de sa source
    def create_document(doc_source, *args, **kwargs):
        if doc_source == "reddit":
            return RedditDocument(*args, **kwargs)
        elif doc_source == "arxiv":
            return ArxivDocument(*args, **kwargs)
        else:
            return Document(*args, **kwargs)