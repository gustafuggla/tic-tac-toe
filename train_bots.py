from player import Player
from tic_tac_toe import TicTacToe
import pickle


bot_1 = Player('Bot1', 1, is_bot=True)
bot_2 = Player('Bot2', 2, is_bot=True)
game = TicTacToe(bot_1, bot_2)

for _ in range(1000):
    game.run(silent=True)
    game.reset()

for bot in [bot_1, bot_2]:
    with open(f'{bot.name}.pkl', 'wb') as f:
        pickle.dump(bot.q_table, f)