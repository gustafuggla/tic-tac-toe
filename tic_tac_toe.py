import numpy as np


class TicTacToe:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.reset()

    def reset(self):
        self.board = np.zeros((3, 3), dtype='int')
        self.player_generator = self.create_player_generator()
        self.game_has_ended = False
        self.winner = None
        self.loser = None

    def create_player_generator(self):
        while True:
            for player in [self.player_1, self.player_2]:
                yield player

    def print_board(self):
        print(' '.join([str(x) for x in self.board[0, :]]))
        print(' '.join([str(x) for x in self.board[1, :]]))
        print(' '.join([str(x) for x in self.board[2, :]]))

    # def get_current_state(self) -> str:
    #     return self.board.tostring()
    
    def get_legal_moves(self) -> list[str]:
        legal_moves = []
        for row, col in np.argwhere(self.board == 0):
            legal_moves.append(str(row) + str(col))
        
        return legal_moves

    def check_win_condition(self):
        for row in range(3):
            if np.all(self.board[row, :] == self.player_1.marker):
                self.winner = self.player_1
                self.loser = self.player_2
            elif np.all(self.board[row, :] == self.player_2.marker):
                self.winner = self.player_2
                self.loser = self.player_1
        
        for col in range(3):
            if np.all(self.board[:, col] == self.player_1.marker):
                self.winner = self.player_1
                self.loser = self.player_2
            elif np.all(self.board[:, col] == self.player_2.marker):
                self.winner = self.player_2
                self.loser = self.player_1
        
        for diag in self.get_diagonals():
            if np.all(diag == self.player_1.marker):
                self.winner = self.player_1
                self.loser = self.player_2
            elif np.all(diag == self.player_2.marker):
                self.winner = self.player_2
                self.loser = self.player_1

        if self.winner is not None:
            self.game_has_ended = True
        elif not self.get_legal_moves():
            self.game_has_ended = True

    def get_diagonals(self) -> list[np.ndarray]:
        diag_1 = np.array([
            self.board[0, 0],
            self.board[1, 1],
            self.board[2, 2],
        ])

        diag_2 = np.array([
            self.board[0, 2],
            self.board[1, 1],
            self.board[2, 0],
        ])

        return [diag_1, diag_2]
    
    def run(self, silent=False):
        active_player = next(self.player_generator)
        while True:
            if not self.game_has_ended:
                if not silent:
                    self.print_board()

                if active_player.is_bot:
                    if not silent:
                        print(f'{active_player.name} is thinking...')
                    move = active_player.make_move(self.board.copy(), self.get_legal_moves())
                else:
                    move = input(f'{active_player.name}, make your move: ').strip()
                
                if move in self.get_legal_moves():
                    row, col = int(move[0]), int(move[1])
                    self.board[row, col] = active_player.marker
                    active_player = next(self.player_generator)
                    self.check_win_condition()
                else:
                    print('Illegal move')
                
            else:
                if self.winner is None:
                    if not silent:
                        print('\nGame is a draw.\n')
                    self.player_1.reward(0)
                    self.player_2.reward(0)

                else:
                    if not silent:
                        print(f'\n{self.winner.name} has won!\n')

                    if self.winner.is_bot:
                        self.winner.reward(1)

                    if self.loser.is_bot:
                        self.loser.reward(-1)
                    
                if not silent:
                    self.print_board()

                break
