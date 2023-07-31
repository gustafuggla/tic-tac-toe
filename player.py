from collections import defaultdict
import numpy as np
import utils


class Player:
    def __init__(self, name, marker, is_bot=False, q_table=None, 
                 learning_rate=0.1, gamma=0.9, epsilon=0.7):
        self.name  = name
        self.is_bot = is_bot
        self.visited_states = []

        assert marker in [1, 2]
        self.marker = marker

        if is_bot:
            if q_table is None:
                self.q_table = defaultdict(int)
            else:
                self.q_table = q_table
            
            self.learning_rate = learning_rate
            self.gamma = gamma
            self.epsilon = epsilon

    def make_move(self, board: np.ndarray, legal_moves: list[str]):
        pre_move_game_state = utils.get_current_state(board)
        self.visited_states.append(pre_move_game_state)
        
        max_value = -np.inf
        if np.random.uniform(0, 1) < self.epsilon:
            for candidate_move in legal_moves:
                temp_board = board.copy()
                row, col = utils.parse_move(candidate_move)
                temp_board[row, col] = self.marker
                candidate_game_state = utils.get_current_state(temp_board)
                candidate_value = self.q_table[candidate_game_state]

                if candidate_value > max_value:
                    max_value = candidate_value
                    move = candidate_move
        else:
            move = np.random.choice(legal_moves)

        row, col = utils.parse_move(move)
        board[row, col] = self.marker
        post_move_game_state = utils.get_current_state(board)
        self.visited_states.append(post_move_game_state)
        
        return move

    def reward(self, reward):
        for game_state in reversed(self.visited_states):
            self.q_table[game_state] += self.learning_rate * \
                (self.gamma * reward - self.q_table[game_state])
            
            reward = self.q_table[game_state]
        
        self.visited_states = []
