from src.word_list import Wordlist

class Game:
    def __init__(self, debug=False):
        self.wordlist = Wordlist()
        self.target_word = self.wordlist.get_random_word().upper()
        self.attempts = 6
        self.debug = debug
        if debug:
            print(f"Mot à trouver : {self.target_word}")
        print(f"Mot à trouver : {self.target_word}")

    def get_feedback(self, guess):
        """Retourne le feedback pour une tentative donnée."""
        guess = guess.upper()
        feedback = []
        target_letters = list(self.target_word)
        
        # Première passe : marquer les lettres correctes (vertes)
        for i in range(len(guess)):
            if guess[i] == target_letters[i]:
                feedback.append(self.color_text(guess[i], "green"))
                target_letters[i] = None  # Marquer la lettre comme utilisée
            else:
                feedback.append(None)  # Placeholder pour la deuxième passe
        
        # Deuxième passe : marquer les lettres présentes mais mal placées (jaunes)
        for i in range(len(guess)):
            if feedback[i] is None:  # Si la lettre n'est pas déjà marquée en vert
                if guess[i] in target_letters:
                    feedback[i] = self.color_text(guess[i], "yellow")
                    # Retirer la première occurrence de la lettre du mot cible
                    target_letters[target_letters.index(guess[i])] = None
                else:
                    feedback[i] = self.color_text(guess[i], "gray")
        
        return " ".join(feedback)

    def color_text(self, text, color):
        """Retourne le texte avec les codes de couleur appropriés."""
        colors = {
            "green": "\033[32m",
            "yellow": "\033[33m",
            "gray": "\033[90m",
            "reset": "\033[0m"
        }
        return f"{colors[color]}{text}{colors['reset']}"

    def validate_guess(self, guess):
        """Valide une tentative et retourne les erreurs éventuelles."""
        errors = []
        if not guess.isalpha():
            errors.append("Le mot ne doit contenir que des lettres.")
        if len(guess) != 5:
            errors.append("Le mot doit contenir exactement 5 lettres.")
        return errors

    def start(self):
        """Démarre le jeu."""
        print("Bienvenue dans le jeu Wordle !")
        print("Devinez le mot de 5 lettres en majuscules.")
        
        while self.attempts > 0:
            print(f"\nTentative {7 - self.attempts}/6")
            guess = input("Votre mot : ").strip().upper()
            
            errors = self.validate_guess(guess)
            if errors:
                for error in errors:
                    print(error)
                continue

            if guess == self.target_word:
                print("\n" + self.color_text("Félicitations ! Vous avez trouvé le mot !", "green"))
                return True

            feedback = self.get_feedback(guess)
            print(f"Indice : {feedback}")
            self.attempts -= 1

        print(f"\nPerdu ! Le mot était : {self.target_word}")
        return False
