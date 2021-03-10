import random

default_options = ['rock', 'paper', 'scissors']
result = ''
counter = 0


def start(user):
    global counter
    print(f'Hello, {user}')
    highscores = open('rating.txt', 'r')
    names = []
    for line in highscores:
        names.append(line.split())
    find_username = [name for name in names if name[0] == user]
    if len(find_username) != 0:
        counter = int(find_username[0][1])
    highscores.close()


def points(score):
    global counter
    if 'draw' in score:
        counter += 50
    elif 'Well done' in score:
        counter += 100


def find_winner(move1, move2):
    global options
    global result
    possible_combinations = []
    possible_combinations.extend(options[options.index(move1) + 1:])
    possible_combinations.extend(options[0:options.index(move1)])
    divisor = len(possible_combinations) / 2
    move1_lose = possible_combinations[0:int(divisor)]
    move1_win = possible_combinations[int(divisor):]
    if move1 == move2:
        result = f'There is a draw ({move1})'
    if move2 in move1_lose:
        result = f'Well done. Computer chose {move1} and failed'
    elif move2 in move1_win:
        result = f'Sorry, but computer chose {move1}'


username = input('Enter your name: ')
start(username)
user_options = input()
if user_options == '':
    options = default_options
else:
    options = user_options.split(',')
print('Okay, let\'s start')

while True:
    computer_choice = random.choice(options)
    user_choice = input()
    if user_choice == '!exit':
        print('Bye!')
        break
    elif user_choice == '!rating':
        print(f'Your rating: {counter}')
    elif user_choice not in options:
        print('Invalid input')
    else:
        find_winner(computer_choice, user_choice)
        print(result)
        points(result)
