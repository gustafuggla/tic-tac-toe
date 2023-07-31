import numpy as np


def parse_move(move: str) -> tuple[int, int]:
    row, col = int(move[0]), int(move[1])
    
    return row, col


def get_current_state(board: np.ndarray) -> str:
    return str(board.reshape(9))