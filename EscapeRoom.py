import random

# Define the escape room as a list of rooms with increasing difficulty
escape_room = [
    {
        'name': 'Entrance Hall',
        'description': 'You are in the Entrance Hall of the escape room. You see a locked door ahead. '
                       'To open it, you need to answer a riddle:',
        'riddle': 'I am taken from a mine, and shut up in a wooden case, from which I am never released, '
                  'and yet I am used by almost every person. What am I?',
        'answer': 'pencil',
    },
    {
        'name': 'Library',
        'description': 'You enter the Library. There is a bookshelf with various books. You need to find a book '
                       'that contains a clue to open the next door.',
        'clue': 'The clue is hidden in the book titled "The Art of Deduction."',
    },
    {
        'name': 'Puzzle Room',
        'description': 'You enter the Puzzle Room. There is a table with a jigsaw puzzle on it. You must complete '
                       'the puzzle to reveal the code to unlock the next door.',
        'puzzle_solution': '1234',
    },
    {
        'name': 'Treasure Room',
        'description': 'You find the Treasure Room. There are three chests, each with a lock. To open them, '
                       'you need to answer a question:',
        'question': 'What has keys but can\'t open locks?',
        'answer': 'a piano',
    },
    {
        'name': 'Escape!',
        'description': 'Congratulations! You have successfully escaped from the escape room!',
    },
]

# Initialize the player's position in the escape room
current_position = 0

# Number of tries for questions
max_question_tries = 3

# Main game loop
while current_position < len(escape_room):
    room = escape_room[current_position]
    print(f'You are in the {room["name"]}.')
    print(room['description'])

    if 'riddle' in room:
        tries = 0
        while tries < max_question_tries:
            user_answer = input('Your answer: ').lower()
            if user_answer == room['answer']:
                print('Correct!\n')
                current_position += 1
                break
            else:
                tries += 1
                if tries < max_question_tries:
                    print('Incorrect answer. Try again.')
                else:
                    print('Oops! You have failed the riddle. The walls start closing in.\n')
                    break

    elif 'clue' in room:
        print(f'Hint: {room["clue"]}\n')
        current_position += 1
    elif 'puzzle_solution' in room:
        user_solution = input('Enter the puzzle solution: ')
        if user_solution == room['puzzle_solution']:
            print('Puzzle solved!\n')
            current_position += 1
        else:
            print('Incorrect solution. Keep trying.\n')
    elif 'question' in room:
        tries = 0
        while tries < max_question_tries:
            user_answer = input('Your answer: ').lower()
            if user_answer == room['answer']:
                print('Correct!\n')
                current_position += 1
                break
            else:
                tries += 1
                if tries < max_question_tries:
                    print('Incorrect answer. Try again.')
                else:
                    print('Oops! You have failed the question. The walls start closing in.\n')
                    break

print("Congratulations! You have successfully escaped from the escape room!")
