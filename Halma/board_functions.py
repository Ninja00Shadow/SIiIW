import numpy as np

def initialize_game_board_13():
    board = np.zeros((16, 16), dtype=int)

    player_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1)]
    player_2 = [(12, 14), (12, 15), (13, 13), (13, 14), (13, 15), (14, 12), (14, 13), (14, 14), (14, 15), (15, 12),
                (15, 13), (15, 14), (15, 15)]

    for x, y in player_1:
        board[x][y] = 1

    for x, y in player_2:
        board[x][y] = 2

    return board


def initialize_game_board_19():
    board = np.zeros((16, 16), dtype=int)

    player_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2),
                (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
    player_2 = [(11, 14), (11, 15), (12, 13), (12, 14), (12, 15), (13, 12), (13, 13), (13, 14), (13, 15), (14, 11),
                (14, 12), (14, 13), (14, 14), (14, 15), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]

    for x, y in player_1:
        board[x][y] = 1

    for x, y in player_2:
        board[x][y] = 2

    return board


def check_game_finished(board):
    player_2 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2),
                (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
    player_1 = [(11, 14), (11, 15), (12, 13), (12, 14), (12, 15), (13, 12), (13, 13), (13, 14), (13, 15), (14, 11),
                (14, 12), (14, 13), (14, 14), (14, 15), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]

    player_1_count = 0
    player_2_count = 0

    for x, y in player_1:
        if board[x][y] == 1:
            player_1_count += 1

    for x, y in player_2:
        if board[x][y] == 2:
            player_2_count += 1

    if player_1_count == 19:
        return 1

    if player_2_count == 19:
        return 2

    return 0