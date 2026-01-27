from game import LetterStatus

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_YELLOW = "\033[43m"
COLOR_RED = "\033[41m"


def display_game(game) -> None:
    for guess in game.guesses:
        for letter, state in guess:
            if state == LetterStatus.WRONG:
                print(letter, end="")
            elif state == LetterStatus.PRESENT:
                print(f"{COLOR_YELLOW}{letter}{COLOR_RESET}", end="")
            elif state == LetterStatus.CORRECT:
                print(f"{COLOR_RED}{letter}{COLOR_RESET}", end="")
        print()

    if not game.is_finished:
        # Next guess
        print(f"{COLOR_RED}{game._secret_word[0]}{COLOR_RESET}", end="")
        if game.guesses:
            guess = game.guesses[-1]
            for letter, state in guess[1:]:
                if state == LetterStatus.CORRECT:
                    print(f"{COLOR_RED}{letter}{COLOR_RESET}", end="")
                else:
                    print("_", end="")
            print()
        else:
            print("_" * (game.n_letters - 1))

        # Other remaining guesses
        for _ in range(game.n_guesses - len(game.guesses) - 1):
            print("_" * game.n_letters)
