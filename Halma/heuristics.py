import math

import numpy as np
import matplotlib.pyplot as plt

from board_functions import initialize_game_board_19


# def distance_heuristic(state, current_player=1):
#     player_target = (15, 15) if current_player == 1 else (0, 0)
#     dead_zone = [(11, 13), (12, 12), (13, 11)] if current_player == 1 else [(4, 2), (3, 3), (2, 4)]
#     golden_zone = [(11, 15), (11, 14), (13, 13), (15, 11), (14, 11)] if current_player == 1 else [(0, 4), (1, 4),
#                                                                                                   (2, 2), (4, 0),
#                                                                                                   (4, 1)]
#
#     player_score = 0
#
#     if check_game_finished(state.board) == current_player:
#         return math.inf
#
#     for y in range(16):
#         for x in range(16):
#             if state.board[x][y] == current_player:
#                 distance = math.sqrt((x - player_target[0]) ** 2 + (y - player_target[1]) ** 2)
#                 player_score += 22 - distance
#                 if distance <= 4:
#                     player_score += 5
#
#                 if (x, y) in dead_zone[1]:
#                     player_score -= 20
#                 elif (x, y) in dead_zone:
#                     player_score -= 7
#
#                 if (x, y) in golden_zone:
#                     player_score += 15
#
#     return player_score

def distance_heuristic(state, current_player=1):
    player_target = (15, 15) if current_player == 1 else (0, 0)
    opponent_target = (0, 0) if current_player == 1 else (15, 15)
    # dead_zone_player = {(11, 13), (12, 12), (13, 11)} if current_player == 1 else {(4, 2), (3, 3), (2, 4)}
    dead_zone_player = (12, 12) if current_player == 1 else (3, 3)
    golden_zone_player = {(11, 15), (11, 14), (13, 13), (15, 11), (14, 11)} if current_player == 1 else {(0, 4), (1, 4),
                                                                                                         (2, 2), (4, 0),
                                                                                                         (4, 1)}

    player_score = 0
    opponent_score = 0

    for y in range(16):
        for x in range(16):
            current_piece = state.board[x][y]
            if current_piece == current_player:
                dx, dy = x - player_target[0], y - player_target[1]
                distance = math.sqrt(dx * dx + dy * dy)
                player_score += 22 - distance
                if distance <= 4:
                    player_score += 5

                if (x, y) == dead_zone_player:
                    player_score -= 20
                # elif (x, y) in dead_zone_player:
                #     player_score -= 7

                if (x, y) in golden_zone_player:
                    player_score += 15
            elif current_piece != 0:
                dx, dy = x - opponent_target[0], y - opponent_target[1]
                distance = math.sqrt(dx * dx + dy * dy)
                opponent_score += 22 - distance
                if distance <= 4:
                    opponent_score += 5

    return player_score - opponent_score


def goal_dispersion_heuristic(state, current_player):
    player_target = (15, 15) if current_player == 1 else (0, 0)
    dead_zone = (12, 12) if current_player == 1 else (3, 3)
    center_mass_x = 0
    center_mass_y = 0
    count = 0
    progression_score = 0

    penalty_zone_player_1 = {(0, 0): 10, (0, 1): 8, (0, 2): 6, (0, 3): 4, (0, 4): 2, (1, 0): 8, (1, 1): 6, (1, 2): 4,
                             (1, 3): 2, (1, 4): 1, (2, 0): 6, (2, 1): 4, (2, 2): 2,
                             (2, 3): 1, (3, 0): 4, (3, 1): 2, (3, 2): 1, (4, 0): 2, (4, 1): 1}
    penalty_zone_player_2 = {(11, 14): 1, (11, 15): 2, (12, 13): 1, (12, 14): 2, (12, 15): 4, (13, 12): 1, (13, 13): 2,
                             (13, 14): 4, (13, 15): 6, (14, 11): 1, (14, 12): 2, (14, 13): 4, (14, 14): 6, (14, 15): 8,
                             (15, 11): 2, (15, 12): 4, (15, 13): 6, (15, 14): 8, (15, 15): 10}

    penalty_zone = penalty_zone_player_1 if current_player == 1 else penalty_zone_player_2

    for y in range(16):
        for x in range(16):
            if state.board[x][y] == current_player:
                distance = math.sqrt((x - player_target[0]) ** 2 + (y - player_target[1]) ** 2)
                progression_score += 22 - distance
                if distance <= 5:
                    progression_score += 5
                if x == dead_zone[0] and y == dead_zone[1]:
                    progression_score -= 7
                if (x, y) in penalty_zone:
                    progression_score -= penalty_zone[(x, y)]

                center_mass_x += x
                center_mass_y += y
                count += 1

    if count > 0:
        center_mass_x /= count
        center_mass_y /= count

    dispersion_score = 0
    for y in range(16):
        for x in range(16):
            if state.board[x][y] == current_player:
                distance_to_center = math.sqrt((x - center_mass_x) ** 2 + (y - center_mass_y) ** 2)
                dispersion_score += distance_to_center

    return progression_score * 0.6 + dispersion_score * 0.4


def wall_corner_heuristic(state, current_player):
    target_x, target_y = (15, 15) if current_player == 1 else (0, 0)

    edges_player_1 = {(11, 14): 9, (11, 15): 4, (12, 15): 4, (13, 15): 5, (14, 15): 6, (15, 15): 10,
                      (15, 14): 6, (15, 13): 5, (15, 12): 4, (15, 11): 4, (14, 11): 9}
    edges_player_2 = {(1, 0): 6, (2, 0): 5, (3, 0): 4, (4, 0): 4, (4, 1): 9, (0, 0): 10, (0, 1): 6,
                      (0, 2): 5, (0, 3): 4, (0, 4): 4, (1, 4): 9}

    edge_bonuses = edges_player_1 if current_player == 1 else edges_player_2

    score = 0

    for x in range(16):
        for y in range(16):
            if state.board[x][y] == current_player:
                distance = math.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
                score += 22 - distance

                if (x, y) in edge_bonuses:
                    score += edge_bonuses[(x, y)]

    return score


def distance_visualization():
    game_board_1 = np.zeros((16, 16), dtype=int)
    dead_zone_1 = [(11, 13), (12, 12), (13, 11)]
    dead_zone_2 = [(4, 2), (3, 3), (2, 4)]
    golden_zone_1 = [(11, 15), (11, 14), (15, 11), (14, 11)]
    golden_zone_2 = [(0, 4), (1, 4), (4, 0), (4, 1)]

    for x in range(16):
        for y in range(16):
            distance = math.sqrt((x - 15) ** 2 + (y - 15) ** 2)
            game_board_1[x][y] = 22 - distance
            if distance <= 4:
                game_board_1[x][y] += 5

            if (x, y) == dead_zone_1[1]:
                game_board_1[x][y] -= 20
            elif (x, y) in dead_zone_1:
                game_board_1[x][y] -= 7

            if (x, y) in golden_zone_1:
                game_board_1[x][y] += 15

    print(game_board_1)

    print()

    game_board_2 = np.zeros((16, 16), dtype=int)

    for x in range(16):
        for y in range(16):
            distance = math.sqrt((x - 0) ** 2 + (y - 0) ** 2)
            game_board_2[x][y] = 22 - distance
            if distance <= 4:
                game_board_2[x][y] += 5

            if (x, y) == dead_zone_2[1]:
                game_board_2[x][y] -= 20
            elif (x, y) in dead_zone_2:
                game_board_2[x][y] -= 7

            if (x, y) in golden_zone_2:
                game_board_2[x][y] += 15

    print(game_board_2)

    print()
    print("---------------------------------------------------------------------------------------")
    print()

    return game_board_1, game_board_2


def dispersion_visualization():
    game_board_1 = initialize_game_board_19()

    center_mass_x = 0
    center_mass_y = 0
    count = 0

    penalty_zone_player_1 = {(0, 0): 10, (0, 1): 8, (0, 2): 6, (0, 3): 4, (0, 4): 2, (1, 0): 8, (1, 1): 6, (1, 2): 4,
                             (1, 3): 2, (1, 4): 1, (2, 0): 6, (2, 1): 4, (2, 2): 2,
                             (2, 3): 1, (3, 0): 4, (3, 1): 2, (3, 2): 1, (4, 0): 2, (4, 1): 1}
    penalty_zone_player_2 = {(11, 14): 1, (11, 15): 2, (12, 13): 1, (12, 14): 2, (12, 15): 4, (13, 12): 1, (13, 13): 2,
                             (13, 14): 4, (13, 15): 6, (14, 11): 1, (14, 12): 2, (14, 13): 4, (14, 14): 6, (14, 15): 8,
                             (15, 11): 2, (15, 12): 4, (15, 13): 6, (15, 14): 8, (15, 15): 10}

    for x in range(16):
        for y in range(16):
            distance = math.sqrt((x - 15) ** 2 + (y - 15) ** 2)
            game_board_1[x][y] += 22 - distance
            if distance <= 5:
                game_board_1[x][y] += 5
            if x == 12 and y == 12:
                game_board_1[x][y] -= 7
            if (x, y) in penalty_zone_player_1:
                game_board_1[x][y] -= penalty_zone_player_1[(x, y)]

            game_board_1[x][y] *= 0.6

            center_mass_x += x
            center_mass_y += y
            count += 1

    if count > 0:
        center_mass_x /= count
        center_mass_y /= count

    for y in range(16):
        for x in range(16):
            distance_to_center = math.sqrt((x - center_mass_x) ** 2 + (y - center_mass_y) ** 2)
            game_board_1[x][y] += distance_to_center * 0.4

    print(game_board_1)

    game_board_2 = np.zeros((16, 16), dtype=int)

    return game_board_1, game_board_2


def wall_corner_visualization():
    game_board_1 = np.zeros((16, 16), dtype=int)

    edges_player_1 = {(11, 14): 5, (11, 15): 9, (12, 15): 4, (13, 15): 5, (14, 15): 6, (15, 15): 10,
                      (15, 14): 6, (15, 13): 5, (15, 12): 4, (15, 11): 9, (14, 11): 5}
    edges_player_2 = {(1, 0): 6, (2, 0): 5, (3, 0): 4, (4, 0): 9, (4, 1): 5, (0, 0): 10, (0, 1): 6,
                      (0, 2): 5, (0, 3): 4, (0, 4): 9, (1, 4): 5}

    for x in range(16):
        for y in range(16):
            distance = math.sqrt((x - 15) ** 2 + (y - 15) ** 2)
            game_board_1[x][y] = 22 - distance
            if distance <= 3:
                game_board_1[x][y] += 10

            if (x, y) in edges_player_1:
                game_board_1[x][y] += edges_player_1[(x, y)]

            if x == 12 and y == 12:
                game_board_1[x][y] -= 20

    print(game_board_1)

    print()

    game_board_2 = np.zeros((16, 16), dtype=int)

    for x in range(16):
        for y in range(16):
            distance = math.sqrt((x - 0) ** 2 + (y - 0) ** 2)
            game_board_2[x][y] = 22 - distance
            if distance <= 3:
                game_board_2[x][y] += 10

            if (x, y) in edges_player_2:
                game_board_2[x][y] += edges_player_2[(x, y)]

            if x == 3 and y == 3:
                game_board_2[x][y] -= 20

    print(game_board_2)

    print()
    print("---------------------------------------------------------------------------------------")
    print()

    return game_board_1, game_board_2


def plot_heatmap(data, title='Heatmap', xlabel='X axis', ylabel='Y axis', cmap='viridis'):
    plt.figure(figsize=(10, 8))
    plt.imshow(data, cmap=cmap, aspect='auto', origin='lower')
    plt.colorbar()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(False)

    plt.gca().invert_yaxis()

    plt.show()


if __name__ == '__main__':
    player_1, player_2 = distance_visualization()

    plot_heatmap(player_1, title='Distance Heuristic player 1', xlabel='', ylabel='', cmap='plasma')
    plot_heatmap(player_2, title='Distance Heuristic player 2', xlabel='', ylabel='', cmap='plasma')

    player_1, player_2 = dispersion_visualization()

    plot_heatmap(player_1, title='Dispersion Heuristic player 1', xlabel='', ylabel='', cmap='plasma')
    plot_heatmap(player_2, title='Dispersion Heuristic player 2', xlabel='', ylabel='', cmap='plasma')

    player_1, player_2 = wall_corner_visualization()

    plot_heatmap(player_1, title='Wall Corner Heuristic player 1', xlabel='', ylabel='', cmap='plasma')
    plot_heatmap(player_2, title='Wall Corner Heuristic player 2', xlabel='', ylabel='', cmap='plasma')
