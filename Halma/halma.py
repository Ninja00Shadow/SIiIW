import math

import numpy as np
import time
from copy import deepcopy


class HalmaState:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player

    def generate_moves(self):
        moves = []
        for x in range(16):
            for y in range(16):
                if self.board[x][y] == self.current_player:
                    moves.extend(generate_moves_with_jumps(self.board, self.current_player, x, y))

        moves = set(moves)
        return list(moves)

    def make_move(self, move):
        new_state = deepcopy(self)

        new_state.board[move.end[0]][move.end[1]] = new_state.current_player
        new_state.board[move.start[0]][move.start[1]] = 0

        return new_state

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return str(self.board)


class Move:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def check_if_legal(self, state):
        start_x, start_y = self.start
        end_x, end_y = self.end

        if state.board[start_x][start_y] != state.current_player:
            return False

        if state.board[end_x][end_y] != 0:
            return False

        if abs(end_x - start_x) <= 1 and abs(end_y - start_y) <= 1:
            return True

        return self._check_jumps(start_x, start_y, end_x, end_y, state, set())

    def _check_jumps(self, current_x, current_y, end_x, end_y, state, visited):
        if (current_x, current_y) == (end_x, end_y):
            return True
        visited.add((current_x, current_y))

        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2), (2, 0), (-2, 0), (0, 2), (0, -2)]
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            mx, my = current_x + dx // 2, current_y + dy // 2

            if 0 <= nx < 16 and 0 <= ny < 16 and (nx, ny) not in visited:
                if state.board[nx][ny] == 0 and state.board[mx][my] in [1, 2]:
                    if self._check_jumps(nx, ny, end_x, end_y, state, visited):
                        return True
        return False

    def __str__(self):
        return f"{self.start} -> {self.end}"

    def __repr__(self):
        return f"{self.start} -> {self.end}"


def check_if_legal_2(board, move, current_player):
    start_x, start_y = move.start
    end_x, end_y = move.end

    if board[start_x][start_y] != current_player:
        return False

    if board[end_x][end_y] != 0:
        return False

    if abs(end_x - start_x) <= 1 and abs(end_y - start_y) <= 1:
        return True

    return check_jumps_2(start_x, start_y, end_x, end_y, board, current_player, set())


def check_jumps_2(current_x, current_y, end_x, end_y, board, current_player, visited):
    if (current_x, current_y) == (end_x, end_y):
        return True
    visited.add((current_x, current_y))

    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2), (2, 0), (-2, 0), (0, 2), (0, -2)]
    for dx, dy in directions:
        nx, ny = current_x + dx, current_y + dy
        mx, my = current_x + dx // 2, current_y + dy // 2

        if 0 <= nx < 16 and 0 <= ny < 16 and (nx, ny) not in visited:
            if board[nx][ny] == 0 and board[mx][my] in [1, 2]:
                if check_jumps_2(nx, ny, end_x, end_y, board, current_player, visited):
                    return True
    return False


def generate_moves_with_jumps(board, current_player, x, y, visited=None):
    if visited is None:
        visited = set()
    visited.add((x, y))

    if board[x][y] != current_player:
        return []

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    moves = []
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        jump_x, jump_y = new_x + dx, new_y + dy
        if 0 <= new_x < 16 and 0 <= new_y < 16 and (new_x, new_y) not in visited:
            if board[new_x][new_y] == 0:  # Simple move
                move = Move((x, y), (new_x, new_y))
                if check_if_legal_2(board, move, current_player):
                    moves.append(move)
                moves.append(Move((x, y), (new_x, new_y)))
            elif board[new_x][new_y] in [1, 2] and 0 <= jump_x < 16 and 16 > jump_y >= 0 == board[jump_x][jump_y] and (
            jump_x, jump_y) not in visited:
                move = Move((x, y), (jump_x, jump_y))
                if check_if_legal_2(board, move, current_player):
                    moves.append(move)
                moves.append(Move((x, y), (jump_x, jump_y)))

                moves.extend(generate_moves_with_jumps(board, current_player, jump_x, jump_y, visited.copy()))
    return moves


# def evaluate_board(state, current_player=1):
#     opponent = 2 if current_player == 1 else 1
#
#     player_score = 0
#     opponent_score = 0
#     player_pieces = 0
#     opponent_pieces = 0
#     for y in range(16):
#         for x in range(16):
#             if state.board[x][y] == current_player:
#                 player_score += (15 - x) + (15 - y)
#                 player_pieces += 1
#                 if x == 0 or x == 15 or y == 0 or y == 15:
#                     player_score += 5
#             elif state.board[x][y] == opponent:
#                 opponent_score += x + y
#                 opponent_pieces += 1
#                 if x == 0 or x == 15 or y == 0 or y == 15:
#                     opponent_score += 5
#
#     player_score += (player_pieces - opponent_pieces) * 10
#     return player_score - opponent_score

def evaluate_board(state, current_player=1):
    opponent = 2 if current_player == 1 else 1
    player_target = (15, 15) if current_player == 1 else (0, 0)
    dead_zone = (12, 12) if current_player == 1 else (3, 3)
    # opponent_target = (0, 0) if current_player == 1 else (15, 15)

    score_difference = 0
    # player_pieces = 0
    opponent_pieces = 0

    if check_game_finished(state.board) == current_player:
        return math.inf

    for y in range(16):
        for x in range(16):
            if state.board[x][y] == current_player:
                distance = math.sqrt((x - player_target[0]) ** 2 + (y - player_target[1]) ** 2)
                # player_score = (15 - x) if current_player == 1 else x
                # player_score += (15 - y) if current_player == 1 else y
                player_score = 22 - distance
                # if abs(x - player_target[0]) <= 4 and abs(y - player_target[1]) <= 4:
                #     player_score += 5
                if distance <= 5:
                    player_score += 5

                if x == dead_zone[0] and y == dead_zone[1]:
                    player_score -= 20
                # player_pieces += 1
                score_difference += player_score
            # elif state.board[x][y] == opponent:
            #     opponent_score = (15 - x) if opponent == 1 else x
            #     opponent_score += (15 - y) if opponent == 1 else y
            #     if abs(x - opponent_target[0]) <= 4 and abs(y - opponent_target[1]) <= 4:
            #         opponent_score += 5
            #     opponent_pieces += 1
            #     score_difference -= opponent_score

    # score_difference += (player_pieces - opponent_pieces) * 10
    return score_difference



def minimax_alpha_beta(state, depth, alpha, beta, maximizing_now):
    if depth == 0:
        return evaluate_board(state, state.current_player), None

    if maximizing_now:
        max_eval = float('-inf')
        best_move = None
        for move in state.generate_moves():
            new_state = state.make_move(move)
            new_state.current_player = 2 if state.current_player == 1 else 1
            eval, _ = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in state.generate_moves():
            new_state = state.make_move(move)
            new_state.current_player = 2 if state.current_player == 1 else 1
            eval, _ = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, None


def minimax(state, depth, maximizing_now):
    if depth == 0:
        return evaluate_board(state, state.current_player), None

    if maximizing_now:
        max_eval = float('-inf')
        best_move = None
        for move in state.generate_moves():
            new_state = state.make_move(move)
            new_state.current_player = 2 if state.current_player == 1 else 1
            eval, _ = minimax(new_state, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in state.generate_moves():
            new_state = state.make_move(move)
            new_state.current_player = 2 if state.current_player == 1 else 1
            eval, _ = minimax(new_state, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval, None


def initialize_game_board_13():
    board = np.zeros((16, 16), dtype=int)

    player_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2),  (3, 0), (3, 1)]
    player_2 = [(12, 14), (12, 15), (13, 13), (13, 14), (13, 15), (14, 12), (14, 13), (14, 14), (14, 15), (15, 12), (15, 13), (15, 14), (15, 15)]

    for x, y in player_1:
        board[x][y] = 1

    for x, y in player_2:
        board[x][y] = 2

    return board


def initialize_game_board_19():
    board = np.zeros((16, 16), dtype=int)

    player_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
    player_2 = [(11, 14), (11, 15), (12, 13), (12, 14), (12, 15), (13, 12), (13, 13), (13, 14), (13, 15), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]

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


def play_halma(board):
    state = HalmaState(board, 1)

    while True:
        print(state)

        start_position = input("Wybierz pionek: ")
        end_position = input("Wybierz pole docelowe: ")
        move = Move((int(start_position[0]), int(start_position[1])), (int(end_position[0]), int(end_position[1])))

        if move.check_if_legal(state):
            state = state.make_move(move)
            state.current_player = 2

            ai_move = play_ai(state)
            state = state.make_move(ai_move)
            state.current_player = 1
        else:
            print("Ruch nielegalny")
            continue


def play_halma_ai_vs_ai(board):
    state = HalmaState(board, 1)
    max_depth = 2
    game_round = 0

    while True:
        print("Round: ", game_round)
        print(state)

        # _, ai1_move = minimax(state, max_depth, state.current_player == 1)
        _, ai1_move = minimax_alpha_beta(state, max_depth, float('-inf'), float('inf'), state.current_player == 1)
        print(ai1_move)
        if ai1_move is None:
            print(state.generate_moves().__len__())
        state = state.make_move(ai1_move)
        state.current_player = 2

        # _, ai2_move = minimax(state, max_depth, state.current_player == 2)
        _, ai2_move = minimax_alpha_beta(state, max_depth, float('-inf'), float('inf'), state.current_player == 2)
        print(ai2_move)
        if ai2_move is None:
            print(state.generate_moves().__len__())
        state = state.make_move(ai2_move)
        state.current_player = 1

        if check_game_finished(state.board) != 0:
            print("Game finished")
            print("Winner: ", check_game_finished(state.board))
            print(state.board)
            break

        game_round += 1


def play_ai(state):
    max_depth = 3

    _, best_move = minimax(state, max_depth, state.current_player == 2)

    return best_move


if __name__ == "__main__":
    game_board = initialize_game_board_19()

    # play_halma(game_board)
    play_halma_ai_vs_ai(game_board)


# if __name__ == "__main__":
#     game_board = initialize_game_board()
#     state = HalmaState(game_board, 1)
#     moves = state.generate_moves()
#     for move in moves:
#         print(move)
#         print(state.make_move(move))


# if __name__ == "__main__":
#     game_board = initialize_game_board_13()
#     state = HalmaState(game_board, 1)
#     start_time = time.time()
#     best_eval, best_move = minimax_alpha_beta(state, 3, float('-inf'), float('inf'), True)
#     elapsed_time = time.time() - start_time
#     print(f"Najlepsza ocena: {best_eval}, Najlepszy ruch: {best_move}")
#     print(f"Czas wykonania: {elapsed_time:.2f} sekund")
#
#     start_time = time.time()
#     eval = evaluate_board(state)
#     elapsed_time = time.time() - start_time
#     print(f"Ocena: {eval}")
#     print(f"Czas wykonania: {elapsed_time:.2f} sekund")
