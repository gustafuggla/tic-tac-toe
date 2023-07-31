import pickle
from player import Player
from tic_tac_toe import TicTacToe


def choose_starting_player() -> tuple[int, int]:
    while True:
        player_start = input('Do you want to play first? (y/n)')
        if player_start == 'y':
            return 1, 2
        elif player_start == 'n':
            return 2, 1
    

player_marker, bot_marker = choose_starting_player()

with open(f'Bot{bot_marker}.pkl', 'rb') as f:
    q_table = pickle.load(f)

human = Player(f'Player {player_marker}', player_marker)
bot = Player(f'Player {bot_marker}', bot_marker, is_bot=True,
             q_table=q_table, epsilon=1)

if player_marker == 1:
    game = TicTacToe(human, bot)
else:
    game = TicTacToe(bot, human)

game.run()
