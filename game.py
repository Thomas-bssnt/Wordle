import unicodedata
from enum import Enum
from pathlib import Path
from random import choice
from typing import cast


class LetterStatus(Enum):
    """
    Status of a letter in a Wordle guess.
    """

    WRONG = 0
    PRESENT = 1
    CORRECT = 2


class InvalidInputError(Exception):
    pass


class GameOverError(Exception):
    pass


class Wordle:
    """
    A Wordle-like game engine.
    """

    def __init__(
        self,
        n_letters: int,
        n_guesses: int,
        language: str,
        require_first_letter: bool = False,
    ) -> None:
        self.n_letters: int = n_letters
        self.n_guesses: int = n_guesses
        self.language: str = language
        self.require_first_letter: bool = require_first_letter

        self.guesses: list[tuple[tuple[str, LetterStatus]]] = []
        self.letter_statuses: dict[str, LetterStatus] = {}

        base_path = Path(__file__).parent / "dictionaries"
        secret_path = base_path / f"{language}_secret.txt"
        dictionary_path = base_path / f"{language}.txt"
        self._secret_word_list: list[str] = self._load_words(secret_path)
        self._word_list: list[str] = self._load_words(dictionary_path)

        self._secret_word: str = self._get_random_n_letter_word()

    # ------------------------------------------------------------
    #  PUBLIC API
    # ------------------------------------------------------------

    def make_guess(self, guess: str) -> None:
        """Submit a guess to the game."""
        if self.is_over:
            raise GameOverError("The game has ended. You have no more guesses.")

        guess = self._normalize(guess)

        self._validate_guess(guess)

        checked = self._check_guess(guess)

        self.guesses.append(checked)
        self._update_letter_statuses(checked)

    @property
    def is_over(self) -> bool:
        return len(self.guesses) == self.n_guesses or self.is_success

    @property
    def is_success(self) -> bool:
        return bool(self.guesses) and all(
            status == LetterStatus.CORRECT for _, status in self.guesses[-1]
        )

    @property
    def remaining_guesses(self) -> int:
        return self.n_guesses - len(self.guesses)

    @property
    def solution(self) -> str | None:
        return self._secret_word if self.is_over else None

    @property
    def hint_letters(self) -> list[str]:
        """Hint letters for the next guess."""
        hint = ["_"] * self.n_letters

        if self.require_first_letter:
            hint[0] = self._secret_word[0]
            start_pos = 1
        else:
            start_pos = 0

        for guess in self.guesses:
            for i, (letter, status) in enumerate(guess[start_pos:], start_pos):
                if status == LetterStatus.CORRECT:
                    hint[i] = letter

        return hint

    # ------------------------------------------------------------
    #  INTERNAL LOGIC
    # ------------------------------------------------------------

    def _load_words(self, file_path: Path) -> list[str]:
        """Load all words from dictionary file."""
        with open(file_path) as file:
            words = [self._normalize(word.strip()) for word in file.readlines()]
        return words

    def _get_random_n_letter_word(self) -> str:
        """Select a random n-letter word from the given word list."""
        n_letter_words = [
            word for word in self._secret_word_list if len(word) == self.n_letters
        ]
        return choice(n_letter_words)

    def _validate_guess(self, guess: str) -> None:
        if len(guess) != self.n_letters:
            raise InvalidInputError(f"Guess must be {self.n_letters} letters long.")

        if not guess.isalpha():
            raise InvalidInputError("Guess contains invalid non-letter characters.")

        if self.require_first_letter and guess[0] != self._secret_word[0]:
            raise InvalidInputError(f"Guess must begin with '{self._secret_word[0]}'.")

        if guess not in self._word_list:
            raise InvalidInputError(f"'{guess}' is not in the dictionary.")

    def _check_guess(self, guess: str) -> tuple[tuple[str, LetterStatus]]:
        result: list[tuple[str, LetterStatus] | None] = [None] * self.n_letters
        secret: list[str | None] = list(self._secret_word)

        # First pass: CORRECT
        for i, letter in enumerate(guess):
            if secret[i] == letter:
                result[i] = (letter, LetterStatus.CORRECT)
                secret[i] = None  # Mark as used

        # Second pass: PRESENT / WRONG
        for i, letter in enumerate(guess):
            if result[i] is not None:
                continue
            if letter in secret:
                result[i] = (letter, LetterStatus.PRESENT)
                secret[secret.index(letter)] = None
            else:
                result[i] = (letter, LetterStatus.WRONG)

        return cast(tuple[tuple[str, LetterStatus]], tuple(result))

    def _update_letter_statuses(
        self, checked_guess: tuple[tuple[str, LetterStatus]]
    ) -> None:
        """Update running letter statuses with strongest statuses."""
        for letter, status in checked_guess:
            current = self.letter_statuses.get(letter)
            if current is None or status.value > current.value:
                self.letter_statuses[letter] = status

    # ------------------------------------------------------------
    #  UTILITIES
    # ------------------------------------------------------------

    @staticmethod
    def _normalize(word: str) -> str:
        """Normalize accents and uppercase."""
        return "".join(
            c
            for c in unicodedata.normalize("NFD", word)
            if not unicodedata.combining(c)
        ).upper()
