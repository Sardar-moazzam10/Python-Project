import random



def game_Plan ():
        print("Welcome to Snake Water Gun Game")
        print(" 1.Game Rules \n 2.Play Game \n 3.Exit")

def game_rules():
                print(" Game Rules: \n It’s a 2-player game (You vs Computer).")
                print(" 1 - Snake drinks Water → Snake wins")

                print(" 2 - Water drowns Gun → Water wins")
                print(" 3 - Gun kills Snake → Gun wins")
                print(" 4 - If both players choose the same → It’s a tie")

def play_game():
        player_choice = input("Enter Player choice: ").lower()
        choice = ["snake", "water", "gun"]
        computer_choice = random.choice(choice).lower()
        print("Computer's choice:", computer_choice)

        if player_choice == "snake" and computer_choice == "water":
            print("Player wins:", player_choice)
        elif player_choice == "water" and computer_choice == "gun":
            print("Player wins:", player_choice)
        elif player_choice == "gun" and computer_choice == "snake":
            print("Player wins:", player_choice)
        elif player_choice == "water" and computer_choice == "snake":
            print("Computer wins:", computer_choice)
        elif player_choice == "gun" and computer_choice == "water":
            print("Computer wins:", computer_choice)
        elif player_choice == "snake" and computer_choice == "gun":
            print("Computer wins:", computer_choice)
        elif player_choice == computer_choice:
            print("It's a tie")
        else:
            print("Invalid choice please select coices like snake, water ,gun to win the game", )


def exit_game():
        print("Exiting...")
        print("Thanks for playing")
        exit()
while True:
    game_Plan()
            
    user_choice = int(input("Enter your choice: "))

    if user_choice == 1:
        game_rules()
    elif user_choice == 2:
        play_game()
    elif user_choice == 3:
        exit_game()
    else:
        print("Invalid choice")

    play_again = input("\nDo you want to play again? (yes/no): ").lower()

    if play_again != "yes":  # If they say 'no', we stop
        print("Thanks for playing! Goodbye 👋")
        break
