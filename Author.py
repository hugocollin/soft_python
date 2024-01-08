class Author:
    # Constructeur de la classe Author
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

    # Méthode pour ajouter un document à la production de l'auteur
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)