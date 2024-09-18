from functools import lru_cache
import numpy as np
import random
import time
import math
from Tree import Tree, Node
from Board import *
import concurrent.futures
from threading import Thread


class Solver:
    def __init__(self, depth=8, Ai_piece=1, player_piece=2, algorithm="α-β Pruning", draw_tree=False):
        self.max_depth = depth
        self.ai_piece = Ai_piece
        self.player_piece = player_piece
        self.algorithm = algorithm
        self.draw_tree = draw_tree
        self.tree = Tree(root_value=0,
                         root_type="Max") if draw_tree else None  # Initialize the tree if draw_tree is True
        self.node_counter = 0
    def solve(self, board):
        col = None
        value = None
        self.node_counter = 0
        if self.tree is None:
            self.tree = Tree(root_value=0,
                             root_type="Max")
        root_node = self.tree.root if self.draw_tree else None

        if self.algorithm.lower() == "minmax".lower():
            col, value = self.MiniMax(board, 0, True, root_node)
        elif self.algorithm.lower() == "α-β Pruning".lower():
            col, value = self.MiniMax_alpha_beta_pruning(board, 0, -math.inf, math.inf, True, root_node)
        elif self.algorithm.lower() == "ExpectMiniMax".lower():
            col, value = self.ExpectiMiniMax(board, 0, True, root_node)
        print("Num Nodes = ",self.node_counter)


        return col, value

    @lru_cache(maxsize=None)
    def MiniMax_alpha_beta_pruning(self, board, depth, alpha, beta, is_maximizer=True, node=None):
        self.node_counter+=1
        if depth >= self.max_depth or board.available_places == 0:
            if self.draw_tree and node:
                node.value = self.evaluate_board(board)[1]
            return None, self.evaluate_board(board)[1]

        cols = self.get_neighbors(board)
        if is_maximizer:
            value = -math.inf
            best_col = None

            for col in cols:
                board.add_piece(col, self.ai_piece)
                child_node = self.tree.add_node(node, 0, "Min") if self.draw_tree else None
                _, score = self.MiniMax_alpha_beta_pruning(board, depth + 1, alpha, beta, False, child_node)
                board.remove_piece(col)  # Undo move

                if score > value:
                    value = score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            if self.draw_tree and node:
                node.value = value
            return best_col, value
        else:
            value = math.inf
            best_col = None

            for col in cols:
                board.add_piece(col, self.player_piece)
                child_node = self.tree.add_node(node, 0, "Max") if self.draw_tree else None
                _, score = self.MiniMax_alpha_beta_pruning(board, depth + 1, alpha, beta, True, child_node)
                board.remove_piece(col)  # Undo move

                if score < value:
                    value = score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            if self.draw_tree and node:
                node.value = value
            return best_col, value

    @lru_cache(maxsize=None)
    def MiniMax(self, board, depth, is_maximizer=True, node=None):
        self.node_counter += 1
        if depth >= self.max_depth or board.available_places == 0:
            if self.draw_tree and node:
                node.value = self.evaluate_board(board)[1]
            return None, self.evaluate_board(board)[1]

        cols = self.get_neighbors(board)
        if is_maximizer:
            value = -math.inf
            best_col = None

            for col in cols:
                board.add_piece(col, self.ai_piece)
                child_node = self.tree.add_node(node, 0, "Min") if self.draw_tree else None
                _, score = self.MiniMax(board, depth + 1, False, child_node)
                board.remove_piece(col)  # Undo move

                if score > value:
                    value = score
                    best_col = col
            if self.draw_tree and node:
                node.value = value
            return best_col, value
        else:
            value = math.inf
            best_col = None

            for col in cols:
                board.add_piece(col, self.player_piece)
                child_node = self.tree.add_node(node, 0, "Max") if self.draw_tree else None
                _, score = self.MiniMax(board, depth + 1, True, child_node)
                board.remove_piece(col)  # Undo move

                if score < value:
                    value = score
                    best_col = col
            if self.draw_tree and node:
                node.value = value
            return best_col, value

    @lru_cache(maxsize=None)
    def ExpectiMiniMax(self, board, depth, is_maximizer=True, node=None):
        self.node_counter += 1
        if depth >= self.max_depth or board.available_places == 0:
            if self.draw_tree and node:
                node.value = self.evaluate_board(board)[1]
            return None, self.evaluate_board(board)[1]

        cols = self.get_neighbors(board)
        if is_maximizer:
            max_value = -math.inf
            best_col = None

            for col in cols:
                expected_value = 0
                columns, probabilities = self.get_cols(board, col)
                child_node = self.tree.add_node(node, 0, "Chance") if self.draw_tree else None

                for idx, col_to_simulate in enumerate(columns):
                    board.add_piece(col_to_simulate, self.ai_piece)
                    grandchild_node = self.tree.add_node(child_node, 0, "Min") if self.draw_tree else None
                    _, value = self.ExpectiMiniMax(board, depth + 1, False, grandchild_node)
                    board.remove_piece(col_to_simulate)  # Undo move
                    expected_value += probabilities[idx] * value

                if expected_value > max_value:
                    max_value = expected_value
                    best_col = col

            if self.draw_tree and node:
                node.value = max_value
            return best_col, max_value

        else:
            min_value = math.inf
            best_col = None

            for col in cols:
                expected_value = 0
                columns, probabilities = self.get_cols(board, col)
                child_node = self.tree.add_node(node, 0, "Chance") if self.draw_tree else None

                for idx, col_to_simulate in enumerate(columns):
                    board.add_piece(col_to_simulate, self.player_piece)
                    grandchild_node = self.tree.add_node(child_node, 0, "Max") if self.draw_tree else None
                    _, value = self.ExpectiMiniMax(board, depth + 1, True, grandchild_node)
                    board.remove_piece(col_to_simulate)  # Undo move
                    expected_value += probabilities[idx] * value

                if expected_value < min_value:
                    min_value = expected_value
                    best_col = col

            if self.draw_tree and node:
                node.value = min_value
            return best_col, min_value

    def evaluate_board(self, board):
        if board.available_places == 0:
            player_4s = self.count_fours(board.current_state, self.player_piece)
            ai_4s = self.count_fours(board.current_state, self.ai_piece)
            if player_4s > ai_4s:
                return (None, -math.inf)
            elif ai_4s > player_4s:
                return (None, math.inf)
            else:
                return (None, 0)
        else:
            return (None, board.calculate_score(self.ai_piece))

    def get_neighbors(self, board):
        valid_columns = [col for col in range(board.cols) if board.first_empty_tile(col) is not None]
        valid_columns.sort(key=lambda col: self.evaluate_move(board, col), reverse=True)
        return valid_columns

    def evaluate_move(self, board, col):
        temp_board = Board(board)
        temp_board.add_piece(col, self.ai_piece)
        return self.evaluate_board(temp_board)[1]

    def get_cols(self, board, col):
        columns = []
        probability_distribution = []

        if col - 1 >= 0 and board.first_empty_tile(col - 1) is not None:
            columns.append(col - 1)

        if board.first_empty_tile(col) is not None:
            columns.append(col)

        if col + 1 < board.cols and board.first_empty_tile(col + 1) is not None:
            columns.append(col + 1)

        if len(columns) == 3:
            probability_distribution = [0.2, 0.6, 0.2]
        elif len(columns) == 2:
            probability_distribution = [0.6, 0.4] if columns[0] == col else [0.4, 0.6]
        elif len(columns) == 1:
            probability_distribution = [1.0]

        return columns, probability_distribution

    def count_fours(self, board, piece):
        count = 0
        rows, cols = board.shape
        # Count all horizontal, vertical, and diagonal sequences of 4 connected pieces
        for r in range(rows):
            for c in range(cols - 3):
                if np.all(board[r, c:c + 4] == piece):
                    count += 1

        for c in range(cols):
            for r in range(rows - 3):
                if np.all(board[r:r + 4, c] == piece):
                    count += 1

        for r in range(rows - 3):
            for c in range(cols - 3):
                if np.all([board[r + i, c + i] == piece for i in range(4)]):
                    count += 1

        for r in range(3, rows):
            for c in range(cols - 3):
                if np.all([board[r - i, c + i] == piece for i in range(4)]):
                    count += 1

        return count


if __name__ == "__main__":
    board = Board()
    c = 0
    while board.available_places >= 0:
        if c % 2 == 0:
            solver = Solver(depth=8, draw_tree=False)
            st = time.time()
            col_1, value = solver.solve(board)
            end = time.time()
            t2 = float(end - st)
            print(f"Time taken  = {t2:.2f} Col = {col_1}")
            board.add_piece(col_1, 1.0)
        else:
            print(board)
            col = int(input("Enter Column: "))
            board.add_piece(col, 2.0)
        c += 1
        if solver.draw_tree:
            thread = Thread(target=solver.tree.draw_tree)
            thread.start()


    print(board.available_places)
