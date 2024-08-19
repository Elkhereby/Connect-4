import numpy as np
from Board import Board
import random
import time
from functools import lru_cache
import math
class Solver:
    def __init__(self,depth=5,Ai_piece=1,player_piece=2):
        self.max_depth = depth
        self.ai_piece = Ai_piece
        self.player_piece = player_piece



    def solve(self,board,solver="minmax"):
        col=None
        value = None
        if solver.lower()=="minmax":
            col,value = self.MiniMax(board,0,True)
        elif solver.lower()=="alphabetapruning":
            col,value = self.MiniMax_alpha_beta_pruning(board,0,-math.inf,math.inf,True)
        elif solver.lower()=="ExpectMiniMax".lower():
            col,value = self.ExpectiMiniMax(board,0,True)
        return col,value


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


    def MiniMax(self,board,depth,is_maximizer=True,):
        if depth>=self.max_depth or board.available_places==0:
            if board.available_places==0:
                player_4s = self.count_fours(board.current_state,self.player_piece)
                ai_4s = self.count_fours(board.current_state,self.ai_piece)
                if player_4s>ai_4s:
                    return (None,-math.inf)
                elif ai_4s>player_4s:
                    return (None,math.inf)
                elif player_4s==ai_4s:
                    return (None,0)
            else:
                return (None,board.calculate_score(self.ai_piece))

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
    def get_cols(self,board,col):
        if col == 0:  # Left edge
            probability_distribution = [0.6, 0.4]
            columns = [col, col + 1]
        elif col == board.cols - 1:  # Right edge
            probability_distribution = [0.4, 0.6]
            columns = [col - 1, col]
        else:
            probability_distribution = [0.2, 0.6, 0.2]
            columns = [col - 1, col, col + 1]
        return columns,probability_distribution

    def ExpectiMiniMax(self, board, depth, is_maximizer=True):
        if depth >= self.max_depth or board.available_places == 0:
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
            col_1, value = solver.solve(board,solver="alphabetapruning")
            end = time.time()
            t2 = float(end-st)





            print(f"Time taken  By AlphaBetaPruning = {t2:.2f} By AlphaBeta Pruning = {col_1}")
            board.add_piece(col_1,1.0)

        else:
            print(board)
            col = int(input(("Enter Column: ")))
            board.add_piece(col,2.0)
        c+=1
