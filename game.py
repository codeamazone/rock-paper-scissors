import random
from pathlib import Path


class RockPaperScissors:
    options = ('rock', 'paper', 'scissors')

    def __init__(self, player):
        self.player = player
        self.score = 0
        self.outcome = ''
        self.rating_path = Path(__file__).parent / 'rating.txt'

    def start(self):
        print(f'Hello, {self.player}')
        highscores = open(self.rating_path, 'r')
        names = []
        for line in highscores:
            names.append(line.split())
        find_player = [name for name in names if name[0] == self.player]
        if len(find_player) != 0:
            self.score = int(find_player[0][1])
        highscores.close()

    def set_options(self):
        """TODO: implement validation of user input to prevent:
                    - even number of options
                    - repeating the same option(s)
                    - just one option
                    - too many options
                 option to enter whitespace separated options"""

        custom_options = input('\nEnter an odd number of custom options, separated by commas.\n'
                               'If you want to play with the default setting, just press "Enter":\nyour options: ')
        if custom_options != '':
            self.options = [option.strip() for option in custom_options.split(',')]

    def update_score(self, score_text):
        if 'draw' in score_text:
            self.score += 50
        elif 'Well done' in score_text:
            self.score += 100

    def determine_winner(self, choice1, choice2):
        index = self.options.index(choice1)
        possible_combinations = self.options[index + 1:] + self.options[:index]
        divisor = len(possible_combinations) / 2
        choice1_lose = possible_combinations[:int(divisor)]
        choice1_win = possible_combinations[int(divisor):]
        if choice1 == choice2:
            self.outcome = f'There is a draw ({choice1})'
        if choice2 in choice1_lose:
            self.outcome = f'Well done. Computer chose {choice1} and failed'
        elif choice2 in choice1_win:
            self.outcome = f'Sorry, but computer chose {choice1}'

    def computer_move(self):
        move = random.choice(self.options)
        return move

    def play_game(self):
        self.start()
        self.set_options()
        print("OK, let's start.")
        while True:
            # computer_choice = random.choice(self.options)
            computer_choice = self.computer_move()
            user_choice = input('\nEnter your choice.\n'
                                'To see your rating, enter "rating", to end the game, enter "exit":\nyour choice: ')
            if user_choice == 'exit':
                print('Bye!')
                break
            elif user_choice == 'rating':
                print(f'Your rating: {self.score}')
            elif user_choice not in self.options:
                print('Invalid input')
            else:
                self.determine_winner(computer_choice, user_choice)
                print(self.outcome)
                self.update_score(self.outcome)


if __name__ == '__main__':
    player_name = input('Enter your name: ')
    game = RockPaperScissors(player_name)
    game.play_game()
