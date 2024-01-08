from Author import Author
from Document import Document, RedditDocument, ArxivDocument
from Corpus import Corpus

import unittest
import numpy as np

# Tests sur les classes du module Author
# Tests sur les méthodes de la classe Author
class TestAuthor(unittest.TestCase):
    # Initialisation des variables de test
    def setUp(self):
        nom_auteur = "Auteur" # Cette valeur peut être modifiée à des fins de test
        self.author = Author(nom_auteur)

    # Test du constructeur de la classe Author
    def test_init(self):
        nom_auteur = "Auteur" # Cette valeur peut être modifiée à des fins de test
        nb_documents = 0      # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.author.name, nom_auteur)
        self.assertEqual(self.author.ndoc, nb_documents)
        self.assertEqual(self.author.production, [])

    # Test de la méthode add de la classe Author
    def test_add(self):
        nom_document = "Document1"      # Cette valeur peut être modifiée à des fins de test
        nb_documents = 1                # Cette valeur peut être modifiée à des fins de test
        liste_documents = ["Document1"] # Cette valeur peut être modifiée à des fins de test
        self.author.add(nom_document)
        self.assertEqual(self.author.ndoc, nb_documents)
        self.assertEqual(self.author.production, liste_documents)

        nom_document = "Document2"                   # Cette valeur peut être modifiée à des fins de test
        nb_documents = 2                             # Cette valeur peut être modifiée à des fins de test
        liste_documents = ["Document1", "Document2"] # Cette valeur peut être modifiée à des fins de test
        self.author.add(nom_document)
        self.assertEqual(self.author.ndoc, nb_documents)
        self.assertEqual(self.author.production, liste_documents)

### Tests sur les classes du module Document
# Tests sur les méthodes de la classe Document
class TestDocument(unittest.TestCase):
    # Initialisation des variables de test
    def setUp(self):
        self.doc = Document("Titre", "Auteur", "Date", "URL", "Texte", "Source")

    # Test de la méthode get_source de la classe Document
    def test_get_source(self):
        source = "Source" # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_source(), source)

    # Test de la méthode get_nb_caracteres de la classe Document
    def test_get_nb_caracteres(self):
        nb_caracteres = 5 # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_nb_caracteres(), nb_caracteres)

    # Test de la méthode get_nb_mots de la classe Document
    def test_get_nb_mots(self):
        nb_mots = 1 # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_nb_mots(), nb_mots)

    # Test de la méthode get_nb_phrases de la classe Document
    def test_get_nb_phrases(self):
        nb_phrases = 0 # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_nb_phrases(), nb_phrases)

# Tests sur les méthodes de la classe RedditDocument
class TestRedditDocument(unittest.TestCase):
    # Initialisation des variables de test
    def setUp(self):
        self.doc = RedditDocument("Titre", "Auteur", "Date", "URL", "Texte", 0, 0.5)

    # Test de la méthode get_source de la classe RedditDocument
    def test_get_source(self):
        source = "Reddit" # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_source(), source)

    # Test de la méthode get_nb_commentaires de la classe RedditDocument
    def test_get_nb_commentaires(self):
        nb_commentaires = 0 # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_nb_commentaires(), nb_commentaires)

    # Test de la méthode get_similarite de la classe RedditDocument
    def test_get_similarite(self):
        similarite = 0.5 # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_similarite(), similarite)
    
    # Test de la méthode __repr__ de la classe RedditDocument
    def test_repr(self):
        expected_output = "\n\nTitre : Titre\nAuteur : Auteur\nDate : Date\nTexte : Texte\nSource : Reddit\nURL : URL\nNombre de commentaires : 0\nStatistiques du document :\n   Pertinence : 50.0%\n   Nombre de caractères : 5\n   Nombre de mots : 1\n   Nombre de phrases : 0\t"
        self.assertEqual(str(self.doc), expected_output)

# Tests sur les méthodes de la classe ArxivDocument
class TestArxivDocument(unittest.TestCase):
    # Initialisation des variables de test
    def setUp(self):
        self.doc = ArxivDocument("Titre", ["Auteur1", "Auteur2"], "Date", "URL", "Texte", 0.5)

    # Test de la méthode get_auteurs de la classe ArxivDocument
    def test_get_auteurs(self):
        auteurs = ["Auteur1", "Auteur2"] # Cette variable peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_auteurs(), auteurs)

    # Test de la méthode get_source de la classe ArxivDocument
    def test_get_source(self):
        source = "Arxiv" # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_source(), source)

    # Test de la méthode get_similarite de la classe ArxivDocument
    def test_get_similarite(self):
        similarite = 0.5 # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.doc.get_similarite(), similarite)
    
    # Test de la méthode __repr__ de la classe ArxivDocument
    def test_repr(self):
        expected_output = "\n\nTitre : Titre\nAuteur : Auteur1\nCo-auteurs : Auteur2\nDate : Date\nTexte : Texte\nSource : Arxiv\nURL : URL\nStatistiques du document :\n   Pertinence : 50.0%\n   Nombre de caractères : 5\n   Nombre de mots : 1\n   Nombre de phrases : 0\t"
        self.assertEqual(str(self.doc), expected_output)

# Tests sur les classes du module Corpus
# Tests sur les méthodes de la classe Corpus
class TestCorpus(unittest.TestCase):
    # Initialisation des variables de test
    def setUp(self):
        self.corpus = Corpus("Mon corpus")

    # Test de la méthode add de la classe Corpus
    def test_add(self):
        self.doc1 = Document("Titre1", "Auteur1", "Date1", "URL1", "Texte1", "Source1") # Cette valeur peut être modifiée à des fins de test
        self.doc2 = Document("Titre2", "Auteur2", "Date2", "URL2", "Texte2", "Source2") # Cette valeur peut être modifiée à des fins de test
        self.corpus.add(self.doc1)
        self.corpus.add(self.doc2)

        self.assertEqual(len(self.corpus.id2doc), 2)
        self.assertEqual(self.corpus.id2doc[1], self.doc1)
        self.assertEqual(self.corpus.id2doc[2], self.doc2)

        self.assertEqual(len(self.corpus.authors), 2)
        nom_auteur = "Auteur1" # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(list(self.corpus.authors.values())[0].name, nom_auteur)
        nom_auteur = "Auteur2" # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(list(self.corpus.authors.values())[1].name, nom_auteur)
    
    # Test de la méthode concat_text de la classe Corpus
    def test_concat_text(self):
        self.test_add()
        self.corpus.concat_text()
        self.resultat_concat = "Texte1\nTexte2" # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(self.corpus.full_text, self.resultat_concat)

    # Test de la méthode search de la classe Corpus
    def test_search(self):
        self.test_concat_text()
        recherche = "Texte1" # Cette valeur peut être modifiée à des fins de test
        passages = self.corpus.search(recherche)
        self.assertEqual(passages, ["Texte1"])

    # Test de la méthode nettoyer_texte de la classe Corpus
    def test_nettoyer_texte(self):
        texte_a_nettoyer = "Test with a ,special, character !" # Cette valeur peut être modifiée à des fins de test
        résultat_nettoyage = "test charact"                    # Cette valeur peut être modifiée à des fins de test
        texte_nettoye = self.corpus.nettoyer_texte(texte_a_nettoyer)
        self.assertEqual(texte_nettoye, résultat_nettoyage)
    
    # Test de la méthode build_vocab de la classe Corpus
    def test_build_vocab(self):
        self.test_add()
        self.corpus.build_vocab()
        vocab_size = 2  # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(len(self.corpus.vocab), vocab_size)
        self.assertIn('texte1', self.corpus.vocab)
        self.assertIn('texte2', self.corpus.vocab)

    # Test de la méthode build_mat_TF de la classe Corpus
    def test_build_mat_TF(self):
        self.test_build_vocab()
        self.corpus.build_vocab()
        self.corpus.build_mat_TF()
        mat_shape = (2, 2)  # Cette valeur peut être modifiée à des fins de test
        self.assertIsNotNone(self.corpus.mat_TF)
        self.assertEqual(self.corpus.mat_TF.shape, mat_shape)

    # Test de la méthode build_mat_TFxIDF de la classe Corpus
    def test_build_mat_TFxIDF(self):
        self.test_build_mat_TF()
        self.corpus.build_vocab()
        self.corpus.build_mat_TF()
        self.corpus.build_mat_TFxIDF()
        mat_shape = (2, 2)  # Cette valeur peut être modifiée à des fins de test
        self.assertIsNotNone(self.corpus.mat_TFxIDF)
        self.assertEqual(self.corpus.mat_TFxIDF.shape, mat_shape)

    # Test de la méthode vectoriser_recherche de la classe Corpus
    def test_vectoriser_recherche(self):
        self.test_add()
        self.corpus.build_vocab()
        recherche = 'Texte1'  # Cette valeur peut être modifiée à des fins de test
        vecteur = self.corpus.vectoriser_recherche(recherche)
        self.assertEqual(vecteur[self.corpus.vocab['texte1']['id']], 1)

    # Test de la méthode calculer_similarites de la classe Corpus
    def test_calculer_similarites(self):
        self.test_build_mat_TFxIDF()
        self.corpus.build_vocab()
        self.corpus.build_mat_TF()
        self.corpus.build_mat_TFxIDF()
        recherche = 'Texte1'  # Cette valeur peut être modifiée à des fins de test
        vecteur = self.corpus.vectoriser_recherche(recherche)
        similarites = self.corpus.calculer_similarites(vecteur)
        taille_similarites = 2  # Cette valeur peut être modifiée à des fins de test
        self.assertEqual(len(similarites), taille_similarites)

if __name__ == '__main__':
    unittest.main()