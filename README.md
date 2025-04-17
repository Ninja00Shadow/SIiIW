# Artificial Intelligence and Knowledge Engineering

This repository contains a collection of mini projects and exercises related to Artificial Intelligence (AI) and Knowledge Engineering. These projects demonstrate various concepts and techniques in the field of AI.

## Projects

### Finding the Shortest Path in a Graph
This project implements **A\*** and **Dijkstra's algorithms** to find the shortest path in a graph. The graph is represented as a dictionary of nodes and their neighbors. The user can input the start and end nodes through a simple command-line interface, and the program will output the shortest path along with its cost.

The graph is based on a list of public transport stations in the city of **Wrocław, Poland**. Each station is a node, and the edges represent the connections between stations (bus and tram routes). Stations are differentiated by their name and coordinates.

This project also includes the **Tabu Search** algorithm as an alternative optimization method.

### Player AI for Halma

This project features an AI player for the game Halma. The AI uses the alpha-beta pruning algorithm to evaluate the game state and make decisions. By default, the game lets two AI players play against each other, but the setup can be easily modified to allow a human player to compete against the AI.

The game is played on a 16x16 board, with each player controlling 19 pieces (a 13-piece version is also available). The goal is to move all of your pieces to the opposite corner of the board. The AI employs a heuristic evaluation function to assess the game state and determine optimal moves.

This project compares the differences between Minimax algorithms (with and without alpha-beta pruning) and evaluates the use of heuristics in decision-making. A detailed explanation of the project is included in the **Sprawozdanie.pdf** file (in Polish).

### Knowledge Base

This project implements a simple knowledge base for troubleshooting washing machines. It uses a set of rules and facts to help diagnose potential issues with a washing machine. The knowledge base was developed using the [Experta library](https://experta.readthedocs.io/en/latest/).

A few test cases are included to demonstrate how the knowledge base functions.

### Machine Learning

This project includes two Jupyter notebooks found in the MachineLearning folder. While the notebooks are mostly in Polish, the code itself is written in English. The notebooks are:

- List4: This notebook uses the scikit-learn library to test several basic classifiers on a T-shirt size dataset. The dataset is small and consists of a few features. Notebook covers the entire machine learning pipeline, from data visualization and splitting the dataset into training and test sets, to processing the data, training classifiers, and evaluating their performance. The classifiers used are:
    - Naive Bayes
    - Decision Tree
    - Random Forest
- List 5: This notebook employs neural networks to predict how funny a joke is. The notebook uses NLP and embeddings (pre-provided) for feature extraction. The notebook trains a neural network model using MLP (Multi-layer Perceptron) and evaluates its performance on the test set. It also analyzes and compares the importance of model parameters. A few test cases are included.