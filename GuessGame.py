# Name: Guessgame.py
# Written by: Triumph Ogbonnia
# Purpose: Generate random number between 1 and user's input
import random
def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    
    # Set the range for the random number
    lower_limit = 1
    upper_limit = 100
    target_number = random.randint(lower_limit, upper_limit)
    
    attempts = 0

    while True:
        user_guess = int(input(f"Guess the number between {lower_limit} and {upper_limit}: "))
        attempts += 1

        if user_guess == target_number:
            print(f"Congratulations! You guessed the number {target_number} in {attempts} attempts.")
            break
        elif user_guess < target_number:
            print("Too low! Try again.")
        else:
            print("Too high! Try again.")

    play_again = input("Do you want to play again? (yes/no): ")
    if play_again.lower() == 'yes':
        number_guessing_game()
    else:
        print("Thanks for playing!")

# Start the game
number_guessing_game()
