import numpy as np
from Board import Board
import random
import time
from functools import lru_cache
import math
class Solver:
    def __init__(self,depth=8,Ai_piece=1,player_piece=2):
        self.max_depth = depth
        self.ai_piece = Ai_piece
        self.player_piece = player_piece
        self.algorithm = "MinMax"

    def solve(self, board):
        col = None
        value = None
        if self.algorithm.lower() == "minmax":
            col, value = self.MiniMax(board, 0, True)
        elif self.algorithm.lower() == "α-βpruning":
            col, value = self.MiniMax_alpha_beta_pruning(board, 0, -math.inf, math.inf, True)
        elif self.algorithm.lower() == "ExpectMiniMax".lower():
            col, value = self.ExpectiMiniMax(board, 0, True)
        return col, value


    def count_fours(self,board, piece):
        count = 0
        rows,cols = board.shape
        # Count all horizontal, vertical, and diagonal sequences of 4 connected pieces
        # Horizontal
        for r in range(rows):
            for c in range(cols - 3):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    count += 1

        # Vertical
        for c in range(cols):
            for r in range(rows - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    count += 1

        # Diagonals (positive slope)
        for r in range(rows - 3):
            for c in range(cols - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    count += 1

        # Diagonals (negative slope)
        for r in range(3, rows):
            for c in range(cols - 3):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    count += 1

        return count

    def MiniMax_alpha_beta_pruning(self, board, depth, alpha, beta, is_maximizer=True):
        if depth >= self.max_depth or board.available_places == 0:
            return self.evaluate_leaf(board)

        if is_maximizer:
            value = -math.inf
            best_col = None
            cols = self.get_neighbors(board)  # Now only returns valid columns

            for col in cols:
                neighbor = Board(board)
                neighbor.add_piece(col, self.ai_piece)
                _, score = self.MiniMax_alpha_beta_pruning(neighbor, depth + 1, alpha, beta, False)
                if score > value:
                    value = score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value = math.inf
            best_col = None
            cols = self.get_neighbors(board)  # Now only returns valid columns

            for col in cols:
                neighbor = Board(board)
                neighbor.add_piece(col, self.player_piece)
                _, score = self.MiniMax_alpha_beta_pruning(neighbor, depth + 1, alpha, beta, True)
                if score < value:
                    value = score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def get_neighbors(self, board):
        valid_columns = [col for col in range(board.cols) if board.first_empty_tile(col) is not None]
        random.shuffle(valid_columns)
        return valid_columns

    def evaluate_leaf(self,board):
        if board.available_places == 0:
            player_4s = self.count_fours(board.current_state, self.player_piece)
            ai_4s = self.count_fours(board.current_state, self.ai_piece)
            if player_4s > ai_4s:
                return (None, -math.inf)
            elif ai_4s > player_4s:
                return (None, math.inf)
            elif player_4s == ai_4s:
                return (None, 0)
        else:
            return (None, board.calculate_score(self.ai_piece))
    def MiniMax(self,board,depth,is_maximizer=True,):
        if depth>=self.max_depth or board.available_places==0:
            return self.evaluate_leaf(board)

        if is_maximizer:
            value = -math.inf
            cols = self.get_neighbors(board)
            best_col = random.choice(cols)
            for col in cols:
                neighbor = Board(board)
                neighbor.add_piece(col, self.ai_piece)
                _,score = self.MiniMax(neighbor,depth+1,False)
                if score>value:
                    value = score
                    best_col = col
            return best_col,value
        else:
            value = math.inf
            cols = self.get_neighbors(board)
            best_col = random.choice(cols)
            for col in cols:
                neighbor = Board(board)
                neighbor.add_piece(col,self.player_piece)
                _, score = self.MiniMax(neighbor, depth + 1, True)
                if score <value:
                    value = score
                    best_col = col

            return best_col, value

    def get_cols(self, board, col):
        columns = []
        probability_distribution = []

        # Check if the left column exists and has space
        if col - 1 >= 0 and board.first_empty_tile(col - 1) is not None:
            columns.append(col - 1)

        # Check if the current column has space
        if board.first_empty_tile(col) is not None:
            columns.append(col)

        # Check if the right column exists and has space
        if col + 1 < board.cols and board.first_empty_tile(col + 1) is not None:
            columns.append(col + 1)

        # Adjust the probability distribution based on the number of valid columns
        if len(columns) == 3:
            probability_distribution = [0.2, 0.6, 0.2]
        elif len(columns) == 2:
            probability_distribution = [0.6, 0.4] if columns[0] == col else [0.4, 0.6]
        elif len(columns) == 1:
            probability_distribution = [1.0]

        return columns, probability_distribution

    def ExpectiMiniMax(self, board, depth, is_maximizer=True):
        if depth >= self.max_depth or board.available_places == 0:
            return self.evaluate_leaf(board)

        if is_maximizer:
            value = -math.inf
            cols = self.get_neighbors(board)
            best_col = random.choice(cols)
            for col in cols:
                neighbor = Board(board)
                neighbor.add_piece(col, self.ai_piece)
                expected_value = 0
                cols, prob = self.get_cols(board, col)

                # Calculate the expected value for each possible move
                for i in range(len(cols)):
                    new_col = cols[i]
                    if 0 <= new_col < board.cols and board.first_empty_tile(new_col) is not None:
                        new_board = Board(board)
                        new_board.add_piece(new_col, self.ai_piece)
                        _, score = self.ExpectiMiniMax(new_board, depth + 1, False)
                        expected_value += prob[i] * score

                # Update the best move based on the calculated expected value
                if expected_value > value:
                    value = expected_value
                    best_col = col

            return best_col, value

        else:
            value = math.inf
            cols = self.get_neighbors(board)
            best_col = random.choice(cols)
            for col in cols:
                neighbor = Board(board)
                neighbor.add_piece(col, self.player_piece)
                expected_value = 0
                cols, prob = self.get_cols(board, col)

                # Calculate the expected value for each possible move
                for i in range(len(cols)):
                    new_col = cols[i]
                    if 0 <= new_col < board.cols and board.first_empty_tile(new_col) is not None:
                        new_board = Board(board)
                        new_board.add_piece(new_col, self.player_piece)
                        _, score = self.ExpectiMiniMax(new_board, depth + 1, True)
                        expected_value += prob[i] * score

                # Update the best move based on the calculated expected value
                if expected_value < value:
                    value = expected_value
                    best_col = col

            return best_col, value






if __name__=="__main__":
    board = Board()
    c=0
    while board.available_places>=0:
        if c%2==0:
            solver = Solver(depth=8)


            st = time.time()
            solver.algorithm = "minmax"

            col_1, value = solver.solve(board)
            end = time.time()
            t2 = float(end-st)





            print(f"Time taken  = {t2:.2f} Col = {col_1}")
            board.add_piece(col_1,1.0)

        else:
            print(board)
            col = int(input(("Enter Column: ")))
            board.add_piece(col,2.0)
        c+=1
