import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import os 
import sys
import coverage

# Ajouter le répertoire parent au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.game import Game
from src.word_list import Wordlist

class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nInitialisation des tests...")
        # Créer un mock pour Wordlist
        cls.wordlist_mock = MagicMock()
        cls.wordlist_mock.get_random_word.return_value = "APPLE"
        cls.patcher = patch('src.game.Wordlist', return_value=cls.wordlist_mock)
        cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()
        print("\nFin des tests")

    def setUp(self):
        self.game = Game(debug=False)
        print(f"\nMot cible: {self.game.target_word}")

    def test_debug_mode(self):
        """Test le mode debug du jeu."""
        print("\nTest : Mode debug")
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            game = Game(debug=True)
            self.assertIn("Mot à trouver", mock_stdout.getvalue())
        print("✓ Test réussi")

    def test_wordlist(self):
        """Test la classe Wordlist."""
        print("\nTest : Wordlist")
        wordlist = Wordlist()
        word = wordlist.get_random_word()
        self.assertIsInstance(word, str)
        self.assertEqual(len(word), 5)
        print("✓ Test réussi")

    def test_get_feedback_all_correct(self):
        print("\nTest : Toutes les lettres sont correctes")
        guess = "APPLE"
        print(f"Tentative: {guess}")
        feedback = self.game.get_feedback(guess)
        print(f"Feedback: {feedback}")
        self.assertIn("A", feedback)
        self.assertIn("P", feedback)
        self.assertIn("P", feedback)
        self.assertIn("L", feedback)
        self.assertIn("E", feedback)
        print("✓ Test réussi")

    def test_get_feedback_some_correct(self):
        print("\nTest : Certaines lettres sont correctes")
        guess = "APRIC"
        print(f"Tentative: {guess}")
        feedback = self.game.get_feedback(guess)
        print(f"Feedback: {feedback}")
        self.assertIn("A", feedback)  # A est correct
        self.assertIn("P", feedback)  # P est correct
        self.assertIn("R", feedback)  # R n'est pas dans le mot
        self.assertIn("I", feedback)  # I n'est pas dans le mot
        self.assertIn("C", feedback)  # C n'est pas dans le mot
        print("✓ Test réussi")

    def test_get_feedback_repeated_letters(self):
        print("\nTest : Lettres répétées")
        guess = "PAPER"
        print(f"Tentative: {guess}")
        feedback = self.game.get_feedback(guess)
        print(f"Feedback: {feedback}")
        self.assertIn("P", feedback)  # P est dans le mot
        self.assertIn("A", feedback)  # A est correct
        self.assertIn("E", feedback)  # E est dans le mot
        self.assertIn("R", feedback)  # R n'est pas dans le mot
        print("✓ Test réussi")

    def test_get_feedback_all_wrong(self):
        print("\nTest : Toutes les lettres sont incorrectes")
        guess = "QWERT"
        print(f"Tentative: {guess}")
        feedback = self.game.get_feedback(guess)
        print(f"Feedback: {feedback}")
        self.assertIn("Q", feedback)
        self.assertIn("W", feedback)
        self.assertIn("E", feedback)  # E est dans le mot
        self.assertIn("R", feedback)
        self.assertIn("T", feedback)
        print("✓ Test réussi")

    def test_color_text(self):
        green_text = self.game.color_text("A", "green")
        yellow_text = self.game.color_text("A", "yellow")
        gray_text = self.game.color_text("A", "gray")

        self.assertEqual(green_text, "\033[32mA\033[0m")
        self.assertEqual(yellow_text, "\033[33mA\033[0m")
        self.assertEqual(gray_text, "\033[90mA\033[0m")

    def test_validate_guess_valid_word(self):
        print("\nTest : Validation d'un mot valide")
        word = "APPLE"
        print(f"Mot testé: {word}")
        result = self.game.validate_guess(word)
        print(f"Résultat: {result}")
        self.assertEqual(result, [])
        print("✓ Test réussi")

    def test_validate_guess_too_short(self):
        print("\nTest : Validation d'un mot trop court")
        word = "APP"
        print(f"Mot testé: {word}")
        result = self.game.validate_guess(word)
        print(f"Résultat: {result}")
        self.assertEqual(result, ["Le mot doit contenir exactement 5 lettres."])
        print("✓ Test réussi")

    def test_validate_guess_too_long(self):
        print("\nTest : Validation d'un mot trop long")
        word = "APPLES"
        print(f"Mot testé: {word}")
        result = self.game.validate_guess(word)
        print(f"Résultat: {result}")
        self.assertEqual(result, ["Le mot doit contenir exactement 5 lettres."])
        print("✓ Test réussi")

    def test_validate_guess_with_numbers(self):
        print("\nTest : Validation d'un mot avec des chiffres")
        word = "APP1E"
        print(f"Mot testé: {word}")
        result = self.game.validate_guess(word)
        print(f"Résultat: {result}")
        self.assertEqual(result, ["Le mot ne doit contenir que des lettres."])
        print("✓ Test réussi")

    def test_validate_guess_with_spaces(self):
        print("\nTest : Validation d'un mot avec des espaces")
        word = "AP PLE"
        print(f"Mot testé: {word}")
        result = self.game.validate_guess(word)
        print(f"Résultat: {result}")
        self.assertIn("Le mot ne doit contenir que des lettres.", result)
        print(result)
        print("✓ Test réussi")

    def test_validate_guess_empty(self):
        print("\nTest : Validation d'un mot vide")
        word = ""
        print(f"Mot testé: {word}")
        result = self.game.validate_guess(word)
        print(f"Résultat: {result}")
        self.assertIn("Le mot doit contenir exactement 5 lettres.", result)
        print("✓ Test réussi")

    def test_victory(self):
        print("\nTest : Victoire immédiate")
        with patch("builtins.input", return_value="APPLE"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                game = Game(debug=False)
                result = game.start()
                self.assertTrue(result)
                self.assertIn("Félicitations", mock_stdout.getvalue())
        print("✓ Test réussi")

    def test_defeat(self):
        print("\nTest : Défaite après 6 tentatives")
        with patch("builtins.input", side_effect=["WRONG"] * 6):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                game = Game(debug=False)
                result = game.start()
                self.assertFalse(result)
                self.assertIn("Perdu", mock_stdout.getvalue())
        print("✓ Test réussi")

    def test_invalid_input_then_victory(self):
        print("\nTest : Entrée invalide suivie d'une victoire")
        with patch("builtins.input", side_effect=["12345", "APPLE"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                game = Game(debug=False)
                result = game.start()
                self.assertTrue(result)
                output = mock_stdout.getvalue()
                self.assertIn("Le mot ne doit contenir que des lettres", output)
                self.assertIn("Félicitations", output)
        print("✓ Test réussi")

if __name__ == "__main__":
    # Démarrer le coverage
    cov = coverage.Coverage()
    cov.start()
    
    # Lancer les tests
    unittest.main(exit=False)
    
    # Arrêter le coverage et afficher le rapport
    cov.stop()
    cov.save()
    print("\n📊 Rapport de couverture :")
    cov.report()