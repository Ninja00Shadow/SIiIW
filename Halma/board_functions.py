import numpy as np


def initialize_game_board_13():
    board = np.zeros((16, 16), dtype=int)

    player_1 = get_target_positions(2, 13)
    player_2 = get_target_positions(1, 13)

    for x, y in player_1:
        board[x][y] = 1

    for x, y in player_2:
        board[x][y] = 2

    return board


def initialize_game_board_19():
    board = np.zeros((16, 16), dtype=int)

    player_1 = get_target_positions(2)
    player_2 = get_target_positions(1)

    for x, y in player_1:
        board[x][y] = 1

    for x, y in player_2:
        board[x][y] = 2

    return board


def get_target_positions(player, number_of_pieces=19):
    if number_of_pieces == 19:
        if player == 1:
            return [(15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (14, 15), (14, 14), (14, 13), (14, 12),
                    (14, 11), (13, 15), (13, 14), (13, 13), (13, 12), (12, 15), (12, 14), (12, 13), (11, 15), (11, 14)]
        else:
            return [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1),
                    (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
    else:
        if player == 1:
            return [(15, 15), (15, 14), (15, 13), (15, 12), (14, 15), (14, 14), (14, 13), (13, 15), (13, 14), (12, 15),
                    (11, 15), (11, 14), (10, 15), (9, 15), (8, 15), (7, 15), (6, 15), (5, 15), (4, 15)]
        else:
            return [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (3, 0), (4, 0), (4, 1),
                    (5, 0), (5, 1), (6, 0), (6, 1), (7, 0), (7, 1), (8, 0)]


def check_game_finished(board):
    player_2 = get_target_positions(2)
    player_1 = get_target_positions(1)

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
