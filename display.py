from game import LetterStatus

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_YELLOW = "\033[43m"
COLOR_RED = "\033[41m"


def _render_letter(letter: str, status: LetterStatus) -> str:
    """Return a colored version of a letter based on its status."""
    if status == LetterStatus.CORRECT:
        return f"{COLOR_RED}{letter}{COLOR_RESET}"
    if status == LetterStatus.PRESENT:
        return f"{COLOR_YELLOW}{letter}{COLOR_RESET}"
    return letter  # WRONG


def _render_guess_row(guess) -> str:
    """Render a full played guess: all letters with their color."""
    return "".join(_render_letter(letter, status) for letter, status in guess)


def _render_hint_row(game) -> str:
    """
    Render the "hint" row:
    - First letter of the secret (colored red)
    - Correct letters from the previous guess
    - Underscores for the rest
    """

    first_letter = _render_letter(game.first_letter, LetterStatus.CORRECT)

    if not game.guesses:
        # First row of the game => first letter + empty underscores
        return first_letter + "_" * (game.n_letters - 1)

    last_guess = game.guesses[-1]
    row = [first_letter]

    # Skip first letter since it's always known
    for letter, status in last_guess[1:]:
        if status == LetterStatus.CORRECT:
            row.append(_render_letter(letter, status))
        else:
            row.append("_")

    return "".join(row)


def _render_empty_rows(game):
    """Render the remaining rows as underscores."""
    remaining = game.n_guesses - len(game.guesses) - 1
    for _ in range(remaining):
        yield "_" * game.n_letters


def display_game(game) -> None:
    """Main display function: renders full board exactly as before."""
    for guess in game.guesses:
        print(_render_guess_row(guess))

    if not game.is_finished:
        print(_render_hint_row(game))

        for row in _render_empty_rows(game):
            print(row)
