from display import display_game
from game import InvalidInputError, Wordle


def play_wordle(n_letters, n_guesses, language, require_first_letter):
    play_again = True
    while play_again:

        game = Wordle(n_letters, n_guesses, language, require_first_letter)

        display_game(game)
        print()

        while not game.is_finished:
            try:
                game.make_a_guess(input())
            except InvalidInputError as e:
                print(e)
            print()
            display_game(game)
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
    require_first_letter = False
    play_wordle(_n_letters, _n_guesses, _language, require_first_letter)
