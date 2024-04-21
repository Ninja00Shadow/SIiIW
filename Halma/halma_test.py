import numpy as np
import time
from copy import deepcopy
from halma import *


def test_minimax_alpha_beta():
    test_board = np.zeros((16, 16), dtype=int)
    test_board[0][0] = 1  # Pionek gracza 1
    test_board[0][1] = 2  # Pionek gracza 2
    test_board[1][1] = 1  # Kolejny pionek gracza 1
    test_board[1][2] = 2  # Kolejny pionek gracza 2
    test_state = HalmaState(test_board, 1)  # Gracz 1 rozpoczyna

    start_time = time.time()
    best_eval, best_move = minimax_alpha_beta(test_state, 3, float('-inf'), float('inf'), True)
    elapsed_time = time.time() - start_time

    # Wypisanie wyników
    print(f"Najlepsza ocena: {best_eval}, Najlepszy ruch: {best_move}")
    print(f"Czas wykonania: {elapsed_time:.2f} sekund")


if __name__ == "__main__":
    test_minimax_alpha_beta()
