import random
import unicodedata


class Wordle:
    def __init__(self, n_letters: int, n_guesses: int, language: str) -> None:
        self.n_letters: int = n_letters
        self.n_guesses: int = n_guesses
        self.language: str = language

        self._secret_word: str = random.choice(
            self._get_n_letters_words(n_letters, "dictionaries/french_secret.txt")
        )
        self._dictionary: list[str] = self._get_n_letters_words(
            n_letters, "dictionaries/french.txt"
        )

        self.guesses: list[tuple[tuple[str, int]]] = []

    def make_a_guess(self, guess: str) -> None:
        if not self.is_finished:
            guess = self._format_guess(guess)
            if len(guess) == self.n_letters:
                if guess.isalpha():
                    if guess[0] == self._secret_word[0]:
                        if guess in self._dictionary:
                            self.guesses.append(self._check_guess(guess))
                        else:
                            raise InvalidInputError(
                                f"The guess “{guess}” is not in the dictionary."
                            )
                    else:
                        raise InvalidInputError(
                            f"The guess “{guess}” needs to start with the letter {self._secret_word[0]}"
                        )
                else:
                    raise InvalidInputError(
                        f"The guess “{guess}” contains invalid characters."
                    )
            else:
                raise InvalidInputError(
                    f"The guess must have {self.n_letters} letters."
                )
        else:
            raise GameOverError("The game has ended. You have no more guesses.")

    def _check_guess(self, guess: str) -> tuple[tuple[str, int]]:
        guess_checked = []
        letters = list(self._secret_word)
        for i, letter in enumerate(guess):
            if letter in letters:
                letters.remove(letter)
                if letter == self._secret_word[i]:
                    guess_checked.append((letter, 2))
                else:
                    guess_checked.append((letter, 1))
            else:
                guess_checked.append((letter, 0))
        return tuple(guess_checked)

    def display(self) -> None:
        for guess in self.guesses:
            for letter, state in guess:
                if state == 0:
                    print(letter, end="")
                elif state == 1:
                    print("\033[43m" + letter + "\033[0m", end="")
                elif state == 2:
                    print("\033[41m" + letter + "\033[0m", end="")
            print()

        if not self.is_finished:
            # Next guess
            print("\033[41m" + self._secret_word[0] + "\033[0m", end="")
            if self.guesses:
                guess = self.guesses[-1]
                for letter, state in guess[1:]:
                    if state == 2:
                        print("\033[41m" + letter + "\033[0m", end="")
                    else:
                        print("_", end="")
                print()
            else:
                print("_" * (self.n_letters - 1))
            # Other remaining guesses
            for _ in range(self.n_guesses - len(self.guesses) - 1):
                print("_" * self.n_letters)

    @property
    def is_finished(self) -> bool:
        return len(self.guesses) == self.n_guesses or self.is_successful

    @property
    def is_successful(self) -> bool:
        if not self.guesses:
            return False
        return [v for _, v in self.guesses[-1]] == [2] * self.n_letters
        # TODO change self.guesses[-1] == [2] * self.n_letters

    @property
    def solution(self) -> str | None:
        if self.is_finished:
            return self._secret_word
        return None

    @staticmethod
    def _get_n_letters_words(n_letters: int, file_path: str) -> list[str]:
        with open(file_path) as file:
            words = [word.strip().upper() for word in file.readlines()]
        return [word for word in words if len(word) == n_letters]

    @staticmethod
    def _format_guess(word: str) -> str:
        """Remove accents and convert to uppercase."""
        return "".join(
            char
            for char in unicodedata.normalize("NFD", word)
            if not unicodedata.combining(char)
        ).upper()


class InvalidInputError(Exception):
    pass


class GameOverError(Exception):
    pass


def play_wordle(n_letters, n_guesses, language):
    play_again = True
    while play_again:

        game = Wordle(n_letters, n_guesses, language)

        game.display()
        print()

        while not game.is_finished:
            try:
                game.make_a_guess(input())
            except InvalidInputError as e:
                print(e)
            print()
            game.display()
            print()
        if game.is_successful:
            print(f"Félicitation ! Le mot à trouver était bien {game.solution}.")
        else:
            print(f"Dommage... Le mot à trouver était {game.solution}")
        print()

        invalid_input = True
        while invalid_input:
            print()
            print("Voulez-vous faire une autre partie ? (oui | non)")
            choice = input()
            if choice.upper() == "OUI":
                play_again = True
                invalid_input = False
            elif choice.upper() == "NON":
                play_again = False
                invalid_input = False
            else:
                invalid_input = True
        if play_again:
            print("\n" * 50)


if __name__ == "__main__":
    _n_letters = 5
    _n_guesses = 6
    _language = "french"

    play_wordle(_n_letters, _n_guesses, _language)
