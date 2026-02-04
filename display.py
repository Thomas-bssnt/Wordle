import os

from game import LetterStatus

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_YELLOW = "\033[43m"
COLOR_RED = "\033[41m"

_KEYBOARD_ROWS = ["AZERTYUIOP", "QSDFGHJKLM", "WXCVBN"]


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
    - First letter of the secret (colored red) - only if require_first_letter is True
    - Correct letters from the previous guesses (colored red)
    - Underscores for the rest
    """
    return "".join(
        _render_letter(letter, LetterStatus.CORRECT) if letter != "_" else "_"
        for letter in game.hint_letters
    )


def _render_empty_rows(game):
    """Render the remaining rows as underscores."""
    remaining = game.n_guesses - len(game.guesses) - 1
    for _ in range(remaining):
        yield "_" * game.n_letters


def _frame_lines(lines: list[str], n_letters: int) -> list[str]:
    """Add a simple box border around the grid."""
    if not lines:
        return lines

    top = "┌" + "─" * n_letters + "┐"
    bottom = "└" + "─" * n_letters + "┘"

    framed = [top]
    for line in lines:
        framed.append(f"│{line}│")
    framed.append(bottom)

    return framed


def _render_keyboard(game) -> list[str]:
    kb = game.letter_statuses
    lines = []

    for row in _KEYBOARD_ROWS:
        rendered_row = " ".join(
            (
                _render_letter(ch, kb[ch])
                if ch in kb and kb[ch] != LetterStatus.WRONG
                else "_" if ch in kb and kb[ch] == LetterStatus.WRONG else ch
            )
            for ch in row
        )
        lines.append(rendered_row)

    return lines


def display_game(game) -> None:
    """Main display function: renders full board with borders."""
    lines = []

    # 1. Past guesses
    for guess in game.guesses:
        lines.append(_render_guess_row(guess))

    # 2. Next hint + empty rows (only if not finished)
    if not game.is_over:
        lines.append(_render_hint_row(game))
        for row in _render_empty_rows(game):
            lines.append(row)

    # 3. Frame them
    framed_lines = _frame_lines(lines, game.n_letters)

    # 4. Print
    for line in framed_lines:
        print(line)

    # 5. Print keyboard (only if not finished)
    if not game.is_over:
        print()
        for row in _render_keyboard(game):
            print(row)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
