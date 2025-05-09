import math

import numpy as np
import time
from copy import deepcopy

from heuristics import *
from board_functions import initialize_game_board_19, check_game_finished


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
        self.board[move.end[0]][move.end[1]] = self.current_player
        self.board[move.start[0]][move.start[1]] = 0

    def unmove(self, move):
        self.board[move.start[0]][move.start[1]] = self.current_player
        self.board[move.end[0]][move.end[1]] = 0

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return str(self.board)

    def __hash__(self):
        return hash(self.board.tobytes() + bytes([self.current_player]))


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
                # move = Move((x, y), (new_x, new_y))
                # if check_if_legal_2(board, move, current_player):
                #     moves.append(move)
                moves.append(Move((x, y), (new_x, new_y)))
            elif board[new_x][new_y] in [1, 2] and 0 <= jump_x < 16 and 16 > jump_y >= 0 == board[jump_x][jump_y] and (
                    jump_x, jump_y) not in visited:
                # move = Move((x, y), (jump_x, jump_y))
                # if check_if_legal_2(board, move, current_player):
                #     moves.append(move)
                moves.append(Move((x, y), (jump_x, jump_y)))

                moves.extend(generate_moves_with_jumps(board, current_player, jump_x, jump_y, visited.copy()))
    return moves


def minimax_alpha_beta(state, depth, alpha, beta, maximizing_now, heuristic):
    node_count = 1

    if depth == 0:
        return heuristic(state, state.current_player), None, node_count

    if maximizing_now:
        max_eval = float('-inf')
        best_move = None
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            eval, _, nodes_visited = minimax_alpha_beta(state, depth - 1, alpha, beta, False, heuristic)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.unmove(move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move, total_nodes + node_count
    else:
        min_eval = float('inf')
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            eval, _, nodes_visited = minimax_alpha_beta(state, depth - 1, alpha, beta, True, heuristic)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.unmove(move)

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, None, total_nodes + node_count


def minimax(state, depth, maximizing_now, heuristic):
    node_count = 1

    if depth == 0:
        return heuristic(state, state.current_player), None, node_count

    if maximizing_now:
        max_eval = float('-inf')
        best_move = None
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            eval,_, nodes_visited = minimax(state, depth - 1, False, heuristic)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.unmove(move)

            if eval > max_eval:
                max_eval = eval
                best_move = move

        return max_eval, best_move, total_nodes + node_count
    else:
        min_eval = float('inf')
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            eval,_, nodes_visited = minimax(state, depth - 1, True, heuristic)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.unmove(move)
            min_eval = min(min_eval, eval)
        return min_eval, None, total_nodes + node_count


def minimax_alpha_beta_2(state, depth, alpha, beta, maximizing_now):
    node_count = 1

    if depth == 0:
        evals = [distance_heuristic(state, state.current_player),
                 wall_corner_heuristic(state, state.current_player), manhattan_heuristic(state, state.current_player)]
        return max(evals), None, node_count

    if maximizing_now:
        max_eval = float('-inf')
        best_move = None
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            eval, _, nodes_visited = minimax_alpha_beta_2(state, depth - 1, alpha, beta, False)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.unmove(move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move, total_nodes + node_count
    else:
        min_eval = float('inf')
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            eval, _, nodes_visited = minimax_alpha_beta_2(state, depth - 1, alpha, beta, True)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.unmove(move)

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, None, total_nodes + node_count


def play_halma(board):
    state = HalmaState(board, 1)

    while True:
        print(state)

        start_position = input("Wybierz pionek: ")
        end_position = input("Wybierz pole docelowe: ")
        move = Move((int(start_position[0]), int(start_position[1])), (int(end_position[0]), int(end_position[1])))

        if move.check_if_legal(state):
            state.make_move(move)
            state.current_player = 2

            _, ai_move = minimax_alpha_beta(state, 2, float('-inf'), float('inf'), True, heuristic=distance_heuristic)
            state.make_move(ai_move)
            state.current_player = 1
        else:
            print("Ruch nielegalny")
            continue


def play_halma_ai_vs_ai(board):
    state = HalmaState(board, 1)
    depth = 2
    game_round = 0

    while True:
        print("Round: ", game_round)
        print(state)

        # MiniMax player
        # _, ai1_move, _ = minimax(state, max_depth_1, state.current_player == 1, heuristic=distance_heuristic)
        _,ai1_move, _ = minimax_alpha_beta(state, depth, float('-inf'), float('inf'), True,
                                         heuristic=goal_dispersion_heuristic)

        # print(ai1_move)
        state.make_move(ai1_move)
        state.current_player = 2

        # AlphaBeta player
        # _, ai2_move, _ = minimax(state, max_depth_2, state.current_player == 2, heuristic=distance_heuristic)
        _, ai2_move, _ = minimax_alpha_beta(state, depth, float('-inf'), float('inf'), True,
                                         heuristic=goal_dispersion_heuristic)
        # _, ai2_move = minimax_alpha_beta_2(state, max_depth_2, float('-inf'), float('inf'), True)

        # print(ai2_move)
        state.make_move(ai2_move)
        state.current_player = 1

        win = check_game_finished(state.board)
        if win != 0:
            print("Game finished")
            print("Winner: ", win)
            print(state.board)
            break

        game_round += 1


if __name__ == "__main__":
    game_board = initialize_game_board_19()

    start = time.time()
    # play_halma(game_board)
    play_halma_ai_vs_ai(game_board)
    end = time.time()
    print("Time: ", end - start)
