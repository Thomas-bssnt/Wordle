import random
import unicodedata
from enum import Enum
from pathlib import Path


class LetterStatus(Enum):
    """Represents the status of a letter in a Wordle guess."""

    WRONG = 0
    PRESENT = 1
    CORRECT = 2


class InvalidInputError(Exception):
    pass


class GameOverError(Exception):
    pass


class Wordle:
    def __init__(self, n_letters: int, n_guesses: int, language: str, require_first_letter: bool = False) -> None:
        self.n_letters: int = n_letters
        self.n_guesses: int = n_guesses
        self.language: str = language
        self.require_first_letter: bool = require_first_letter

        base_path = Path(__file__).parent / "dictionaries"
        secret_path = base_path / "french_secret.txt"
        dictionary_path = base_path / "french.txt"

        self._secret_word: str = random.choice(
            self._get_n_letters_words(n_letters, secret_path)
        )
        self._dictionary: list[str] = self._get_n_letters_words(
            n_letters, dictionary_path
        )

        self.guesses: list[tuple[tuple[str, LetterStatus]]] = []

    def make_a_guess(self, guess: str) -> None:
        if self.is_finished:
            raise GameOverError("The game has ended. You have no more guesses.")

        guess = self._format_guess(guess)

        if len(guess) != self.n_letters:
            raise InvalidInputError(f"The guess must have {self.n_letters} letters.")

        if not guess.isalpha():
            raise InvalidInputError(f"The guess '{guess}' contains invalid characters.")

        if self.require_first_letter and guess[0] != self._secret_word[0]:
            raise InvalidInputError(
                f"The guess '{guess}' needs to start with the letter {self._secret_word[0]}"
            )

        if guess not in self._dictionary:
            raise InvalidInputError(f"The guess '{guess}' is not in the dictionary.")

        self.guesses.append(self._check_guess(guess))

    def _check_guess(self, guess: str) -> tuple[tuple[str, LetterStatus]]:
        guess_checked = []
        letters = list(self._secret_word)
        for i, letter in enumerate(guess):
            if letter in letters:
                letters.remove(letter)
                if letter == self._secret_word[i]:
                    guess_checked.append((letter, LetterStatus.CORRECT))
                else:
                    guess_checked.append((letter, LetterStatus.PRESENT))
            else:
                guess_checked.append((letter, LetterStatus.WRONG))
        return tuple(guess_checked)

    @property
    def is_finished(self) -> bool:
        return len(self.guesses) == self.n_guesses or self.is_successful

    @property
    def is_successful(self) -> bool:
        if not self.guesses:
            return False
        return all(status == LetterStatus.CORRECT for _, status in self.guesses[-1])

    @property
    def solution(self) -> str | None:
        if self.is_finished:
            return self._secret_word
        return None

    @property
    def first_letter(self) -> str:
        return self._secret_word[0]

    @staticmethod
    def _get_n_letters_words(n_letters: int, file_path: Path) -> list[str]:
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
