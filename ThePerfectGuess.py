import random

class ThePerfectGuess:
    def __init__(self, total_choices=10, computer_choice=None):
        self.total_choices = total_choices
        self.computer_choice = computer_choice

    @staticmethod
    def game_plan():
        print("Welcome To \"The Perfect Guess\" Game 🎯")
        print("1. Game Rules")
        print("2. Play Game")
        print("3. Exit")

    @staticmethod
    def game_rules():
        print("\n📜 Game Rules:")
        print("It’s a 'Perfect Guess' game where you have a limited number of guesses to find the correct number.\n")


class PlayGame(ThePerfectGuess):
    def __init__(self, total_choices=10, computer_choice=None):
        super().__init__(total_choices, computer_choice)
        self.choice_left = total_choices
        self.computer_choice = random.choice(range(1, 50))

    def play_game(self):
        print(f"\nYou have {self.total_choices} chances to guess the correct number!")
        choice_left = self.total_choices

        while choice_left > 0:
            try:
                player_choice = int(input("\nEnter your number: "))
            except ValueError:
                print("❌ Invalid input! Please enter a number.")
                continue

            print(f"Player entered number: {player_choice}")

            if player_choice < self.computer_choice:
                print("Too Low! Try Again.")
            elif player_choice > self.computer_choice:
                print("Too High! Try Again.")
            else:
                print("\n🎉 Congratulations! You guessed it right!")
                print(f"The guessed number was {self.computer_choice}.")
                print(f"You guessed the number with {choice_left - 1} chances left.")
                break

            choice_left -= 1
            print(f"You have {choice_left} choices left.")

        else:
            print("\n❌ Out of chances!")
            print(f"The correct number was: {self.computer_choice}")

    @staticmethod
    def exit_game():
        print("\nExiting...")
        print("Thanks for playing! Goodbye 👋")
        exit()

    def start_game(self):
        while True:
            self.game_plan()
            try:
                user_choice = int(input("\nEnter your choice (1–3): "))
            except ValueError:
                print("❌ Invalid input! Please enter a number.")
                continue

            if user_choice == 1:
                self.game_rules()
            elif user_choice == 2:
                self.play_game()
            elif user_choice == 3:
                self.exit_game()
            else:
                print("❌ Invalid choice! Please select from the menu.")

            play_again = input("\nDo you want to play again? (yes/no): ").lower()
            if play_again != "yes":
                print("\nThanks for playing! Goodbye 👋")
                break


if __name__ == "__main__":
    game = PlayGame()
    game.start_game()
