from display import clear_screen, display_game
from game import InvalidInputError, Wordle


def user_wants_to_play_again() -> bool:
    """Ask the user if they want to play again."""
    while True:
        print("Voulez-vous faire une autre partie ? (oui | non)")
        replay = input().strip().lower()
        if replay == "oui":
            return True
        elif replay == "non":
            return False
        else:
            print("Entrée invalide. Veuillez répondre par 'oui' ou 'non'.")


def get_valid_guess(game: Wordle) -> str:
    """Ask for guesses until a valid one is entered."""
    while True:
        guess = input().strip()
        try:
            game.make_guess(guess)
            return guess
        except InvalidInputError as e:
            print(e)
            print()


def play_round(game: Wordle):
    """Play a full game round."""
    while not game.is_over:
        clear_screen()

        print()
        display_game(game)
        print()

        get_valid_guess(game)

    clear_screen()
    display_game(game)
    print()

    if game.is_success:
        print(f"Félicitation ! Le mot à trouver était bien {game.solution}.")
    else:
        print(f"Dommage... Le mot à trouver était {game.solution}")
    print()


def play_wordle(n_letters, n_guesses, language, require_first_letter):
    game = Wordle(n_letters, n_guesses, language, require_first_letter)

    while True:
        play_round(game)

        if not user_wants_to_play_again():
            break

        game.reset()


if __name__ == "__main__":
    n_letters = 5
    n_guesses = 6
    language = "french"
    require_first_letter = False
    play_wordle(n_letters, n_guesses, language, require_first_letter)
