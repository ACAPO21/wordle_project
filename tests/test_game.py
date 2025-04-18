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
        
        # Vérifier que toutes les lettres sont en vert
        for letter in guess:
            colored_letter = self.game.color_text(letter, "green")
            self.assertIn(colored_letter, feedback)
        print("✓ Test réussi")

    def test_get_feedback_some_correct(self):
        print("\nTest : Certaines lettres sont correctes")
        guess = "APRIC"
        print(f"Tentative: {guess}")
        feedback = self.game.get_feedback(guess)
        print(f"Feedback: {feedback}")
        
        # Vérifier les lettres correctes (vertes)
        green_A = self.game.color_text("A", "green")
        green_P = self.game.color_text("P", "green")
        self.assertIn(green_A, feedback)
        self.assertIn(green_P, feedback)
        
        # Vérifier les lettres absentes (grises)
        gray_R = self.game.color_text("R", "gray")
        gray_I = self.game.color_text("I", "gray")
        gray_C = self.game.color_text("C", "gray")
        self.assertIn(gray_R, feedback)
        self.assertIn(gray_I, feedback)
        self.assertIn(gray_C, feedback)
        print("✓ Test réussi")

    def test_get_feedback_repeated_letters(self):
        print("\nTest : Lettres répétées")
        guess = "PAPER"
        print(f"Tentative: {guess}")
        feedback = self.game.get_feedback(guess)
        print(f"Feedback: {feedback}")
        
        # Vérifier les couleurs exactes
        yellow_P1 = self.game.color_text("P", "yellow")
        yellow_A = self.game.color_text("A", "yellow")
        green_P2 = self.game.color_text("P", "green")
        yellow_E = self.game.color_text("E", "yellow")
        gray_R = self.game.color_text("R", "gray")
        
        self.assertIn(yellow_P1, feedback)
        self.assertIn(yellow_A, feedback)
        self.assertIn(green_P2, feedback)
        self.assertIn(yellow_E, feedback)
        self.assertIn(gray_R, feedback)
        print("✓ Test réussi")

    def test_get_feedback_all_wrong(self):
        print("\nTest : Toutes les lettres sont incorrectes")
        guess = "QWERT"
        print(f"Tentative: {guess}")
        feedback = self.game.get_feedback(guess)
        print(f"Feedback: {feedback}")
        
        # Vérifier que toutes les lettres sont en gris sauf E qui est jaune
        gray_Q = self.game.color_text("Q", "gray")
        gray_W = self.game.color_text("W", "gray")
        yellow_E = self.game.color_text("E", "yellow")  # E est dans le mot mais mal placé
        gray_R = self.game.color_text("R", "gray")
        gray_T = self.game.color_text("T", "gray")
        
        self.assertIn(gray_Q, feedback)
        self.assertIn(gray_W, feedback)
        self.assertIn(yellow_E, feedback)
        self.assertIn(gray_R, feedback)
        self.assertIn(gray_T, feedback)
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
    unittest.main()
    