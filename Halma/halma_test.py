import numpy as np
import time
from halma import *


def test_case_alpha_beta(first_player_heuristic, second_player_heuristic, file_name):
    experimental_file = open(f"experiments/{file_name}", "w")

    for i in range(10):
        board = initialize_game_board_19()
        state = HalmaState(board, 1)
        depth = 2
        experimental_file.write(f"Game {i + 1}\n")
        print(f"Game {i + 1}")

        start_time = time.time()

        game_round = 0
        total_nodes = 0

        while True:
            print(f"Round {game_round + 1}")
            print(state)

            _, ai1_move, visited_nodes = minimax_alpha_beta(state, depth, float('-inf'), float('inf'), True,
                                                            heuristic=first_player_heuristic)

            total_nodes += visited_nodes

            state.make_move(ai1_move)
            state.current_player = 2

            _, ai2_move, visited_nodes = minimax_alpha_beta(state, depth, float('-inf'), float('inf'), True,
                                                            heuristic=second_player_heuristic)

            total_nodes += visited_nodes

            state.make_move(ai2_move)
            state.current_player = 1

            win = check_game_finished(state.board)
            if win != 0:
                experimental_file.write(str(state))
                experimental_file.write("\n")
                experimental_file.write(f"Winner: {win}\n")
                print(f"Winner: {win}")
                break

            game_round += 1

        end_time = time.time()
        experimental_file.write(f"Moves: {game_round}\n")
        experimental_file.write(f"Time: {end_time - start_time}\n")
        experimental_file.write(f"Total nodes visited: {total_nodes}\n")
        experimental_file.write("\n")
        experimental_file.write("\n")


def test_minimax_alone(file_name):
    experimental_file = open(f"experiments/{file_name}", "w")

    for i in range(3):
        board = initialize_game_board_19()
        state = HalmaState(board, 1)
        depth = 2
        experimental_file.write(f"Game {i + 1}\n")
        print(f"Game {i + 1}")

        start_time = time.time()

        game_round = 0
        total_nodes = 0

        while True:
            print(f"Round {game_round + 1}")
            print(state)

            _, ai1_move, visited_nodes = minimax(state, depth, True, heuristic=distance_heuristic)

            total_nodes += visited_nodes

            state.make_move(ai1_move)
            state.current_player = 2

            _, ai2_move, visited_nodes = minimax(state, depth, True, heuristic=distance_heuristic)

            total_nodes += visited_nodes

            state.make_move(ai2_move)
            state.current_player = 1

            win = check_game_finished(state.board)
            if win != 0:
                experimental_file.write(str(state))
                experimental_file.write("\n")
                experimental_file.write(f"Winner: {win}\n")
                print(f"Winner: {win}")
                break

            game_round += 1

        end_time = time.time()
        experimental_file.write(f"Moves: {game_round}\n")
        experimental_file.write(f"Time: {end_time - start_time}\n")
        experimental_file.write(f"Total nodes visited: {total_nodes}\n")
        experimental_file.write("\n")
        experimental_file.write("\n")


def test_case_minimax_vs_alpha_beta(file_name):
    experimental_file = open(f"experiments/{file_name}", "w")

    for i in range(10):
        board = initialize_game_board_19()
        state = HalmaState(board, 1)
        depth = 2
        experimental_file.write(f"Game {i + 1}\n")
        print(f"Game {i + 1}")

        start_time = time.time()

        game_round = 0
        total_nodes = 0

        while True:
            print(f"Round {game_round + 1}")
            print(state)

            _, ai1_move, visited_nodes = minimax(state, depth, True, heuristic=distance_heuristic)

            total_nodes += visited_nodes

            state.make_move(ai1_move)
            state.current_player = 2

            _, ai2_move, visited_nodes = minimax_alpha_beta(state, depth, float('-inf'), float('inf'), True,
                                                            heuristic=distance_heuristic)

            total_nodes += visited_nodes

            state.make_move(ai2_move)
            state.current_player = 1

            win = check_game_finished(state.board)
            if win != 0:
                experimental_file.write(str(state))
                experimental_file.write("\n")
                experimental_file.write(f"Winner: {win}\n")
                print(f"Winner: {win}")
                break

            game_round += 1

        end_time = time.time()
        experimental_file.write(f"Moves: {game_round}\n")
        experimental_file.write(f"Time: {end_time - start_time}\n")
        experimental_file.write(f"Total nodes visited: {total_nodes}\n")
        experimental_file.write("\n")
        experimental_file.write("\n")


def test_improved_alfa_beta(file_name):
    experimental_file = open(f"experiments/{file_name}", "w")

    for i in range(10):
        board = initialize_game_board_19()
        state = HalmaState(board, 1)
        depth = 2
        experimental_file.write(f"Game {i + 1}\n")
        print(f"Game {i + 1}")

        start_time = time.time()

        game_round = 0
        total_nodes = 0

        while True:
            print(f"Round {game_round + 1}")
            print(state)

            _, ai1_move, visited_nodes = minimax_alpha_beta(state, depth, float('-inf'), float('inf'), True,
                                                            heuristic=wall_corner_heuristic)

            total_nodes += visited_nodes

            state.make_move(ai1_move)
            state.current_player = 2

            _, ai2_move, visited_nodes = minimax_alpha_beta_2(state, depth, float('-inf'), float('inf'), True)

            total_nodes += visited_nodes

            state.make_move(ai2_move)
            state.current_player = 1

            win = check_game_finished(state.board)
            if win != 0:
                experimental_file.write(str(state))
                experimental_file.write("\n")
                experimental_file.write(f"Winner: {win}\n")
                print(f"Winner: {win}")
                break

            game_round += 1

        end_time = time.time()
        experimental_file.write(f"Moves: {game_round}\n")
        experimental_file.write(f"Time: {end_time - start_time}\n")
        experimental_file.write(f"Total nodes visited: {total_nodes}\n")
        experimental_file.write("\n")
        experimental_file.write("\n")


if __name__ == "__main__":
    # test_case_alpha_beta(distance_heuristic, distance_heuristic, "distance_heuristic.txt")
    # test_case_alpha_beta(manhattan_heuristic, manhattan_heuristic, "manhattan_heuristic.txt")
    # test_case_alpha_beta(goal_dispersion_heuristic, goal_dispersion_heuristic, "goal_dispersion_heuristic.txt")
    # test_case_alpha_beta(wall_corner_heuristic, wall_corner_heuristic, "wall_corner_heuristic.txt")

    # test_case_alpha_beta(distance_heuristic, manhattan_heuristic, "distance_manhattan.txt")
    # test_case_alpha_beta(distance_heuristic, goal_dispersion_heuristic, "distance_dispersion.txt")
    # test_case_alpha_beta(distance_heuristic, wall_corner_heuristic, "distance_wall_corner.txt")

    # test_case_alpha_beta(manhattan_heuristic, distance_heuristic, "manhattan_distance.txt")
    # test_case_alpha_beta(manhattan_heuristic, goal_dispersion_heuristic, "manhattan_dispersion.txt")
    # test_case_alpha_beta(manhattan_heuristic, wall_corner_heuristic, "manhattan_wall_corner.txt")

    # test_case_alpha_beta(goal_dispersion_heuristic, distance_heuristic, "dispersion_distance.txt")
    # test_case_alpha_beta(goal_dispersion_heuristic, manhattan_heuristic, "dispersion_manhattan.txt")
    # test_case_alpha_beta(goal_dispersion_heuristic, wall_corner_heuristic, "dispersion_wall_corner.txt")

    # test_case_alpha_beta(wall_corner_heuristic, distance_heuristic, "wall_corner_distance.txt")
    # test_case_alpha_beta(wall_corner_heuristic, manhattan_heuristic, "wall_corner_manhattan.txt")
    # test_case_alpha_beta(wall_corner_heuristic, goal_dispersion_heuristic, "wall_corner_dispersion.txt")

    # test_minimax_alone("minimax.txt")
    # test_case_minimax_vs_alpha_beta("minimax_vs_alpha_beta.txt")

    test_improved_alfa_beta("all_heuristics.txt")
