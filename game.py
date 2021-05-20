import random


class RockPaperScissors:
    options = ['rock', 'paper', 'scissors']
    outcome = ''
    counter = 0

    def __init__(self, player):
        self.player = player

    def start(self):
        print(f'Hello, {self.player}')
        highscores = open('rating.txt', 'r')
        names = []
        for line in highscores:
            names.append(line.split())
        find_player = [name for name in names if name[0] == self.player]
        if len(find_player) != 0:
            self.counter = int(find_player[0][1])
        highscores.close()

    def set_options(self):
        custom_options = input('Enter your custom options, separated by a comma and a space.\n'
                               'If you want to play with the default setting, just press "Enter".')
        if custom_options != '':
            self.options = custom_options.split(', ')

    def score(self, score):
        if 'draw' in score:
            self.counter += 50
        elif 'Well done' in score:
            self.counter += 100

    def determine_winner(self, choice1, choice2):
        possible_combinations = []
        possible_combinations.extend(self.options[self.options.index(choice1) + 1:])
        possible_combinations.extend(self.options[0:self.options.index(choice1)])
        divisor = len(possible_combinations) / 2
        choice1_lose = possible_combinations[0:int(divisor)]
        choice1_win = possible_combinations[int(divisor):]
        if choice1 == choice2:
            self.outcome = f'There is a draw ({choice1})'
        if choice2 in choice1_lose:
            self.outcome = f'Well done. Computer chose {choice1} and failed'
        elif choice2 in choice1_win:
            self.outcome = f'Sorry, but computer chose {choice1}'

    def play_game(self):
        self.start()
        self.set_options()
        print("OK, let's start.")
        while True:
            computer_choice = random.choice(self.options)
            user_choice = input('Enter your choice.\n'
                                'To see your rating, enter "rating", to end the game, enter "exit": ')
            if user_choice == 'exit':
                print('Bye!')
                break
            elif user_choice == 'rating':
                print(f'Your rating: {self.counter}')
            elif user_choice not in self.options:
                print('Invalid input')
            else:
                self.determine_winner(computer_choice, user_choice)
                print(self.outcome)
                self.score(self.outcome)


if __name__ == '__main__':
    player_name = input('Enter your name: ')
    game = RockPaperScissors(player_name)
    game.play_game()
