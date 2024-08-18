import numpy as np
from Board import Board
import random
import time
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
            col,value = self.MiniMax_alpha_beta_pruning(board,0,float('-inf'),float('inf'),True)

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
    def MiniMax_alpha_beta_pruning(self, board, depth,alpha,beta, is_maximizer=True):
        if depth >= self.max_depth or board.available_places == 0:
            if board.available_places == 0:
                player_4s = self.count_fours(board.current_state, self.player_piece)
                ai_4s = self.count_fours(board.current_state, self.ai_piece)
                if player_4s > ai_4s:
                    return (None, float('-inf'))
                elif ai_4s > player_4s:
                    return (None, float('inf'))
                elif player_4s == ai_4s:
                    return (None, 0)
            else:
                return (None, board.calculate_score(self.ai_piece))

        if is_maximizer:
            value = float('-inf')
            neighbors = self.get_neighbors(board, self.ai_piece)
            best_col = neighbors[0][0]

            for (col, neighbor) in neighbors:
                _, score = self.MiniMax_alpha_beta_pruning(neighbor, depth + 1,alpha,beta, False)
                alpha = max(value,alpha)
                if alpha>=beta:
                    break
                if score > value:
                    value = score
                    best_col = col
            return best_col, value
        else:
            value = float('inf')
            neighbors = self.get_neighbors(board, self.player_piece)
            best_col = neighbors[0][0]
            for (col, neighbor) in neighbors:
                _, score = self.MiniMax_alpha_beta_pruning(neighbor, depth + 1,alpha,beta, True)
                beta = min(value, beta)
                if alpha>=beta:
                    break
                if score < value:
                    value = score
                    best_col = col

            return best_col, value
    def get_neighbors(self,board,piece):
        valid_locations = []
        cols = list(range(board.cols))
        random.shuffle(cols)# random shuffling so that algorithm doesnt have determenistic patterns
        for i in cols:

            temp_board = Board(board)
            ret = temp_board.add_piece(i,piece)
            if ret:
                valid_locations.append((i,temp_board))
        return valid_locations

    def MiniMax(self,board,depth,is_maximizer=True,):
        if depth>=self.max_depth or board.available_places==0:
            if board.available_places==0:
                player_4s = self.count_fours(board.current_state,self.player_piece)
                ai_4s = self.count_fours(board.current_state,self.ai_piece)
                if player_4s>ai_4s:
                    return (None,float('-inf'))
                elif ai_4s>player_4s:
                    return (None,float('inf'))
                elif player_4s==ai_4s:
                    return (None,0)
            else:
                return (None,board.calculate_score(self.ai_piece))

        if is_maximizer:
            value = float('-inf')
            neighbors = self.get_neighbors(board, self.ai_piece)
            best_col = neighbors[0][0]

            for (col,neighbor) in neighbors:
                _,score = self.MiniMax(neighbor,depth+1,False)
                if score>value:
                    value = score
                    best_col = col
            return best_col,value
        else:
            value = float('inf')
            neighbors = self.get_neighbors(board, self.player_piece)
            best_col = neighbors[0][0]
            for (col,neighbor) in neighbors:
                _, score = self.MiniMax(neighbor, depth + 1, True)
                if score <value:
                    value = score
                    best_col = col

            return best_col, value


if __name__=="__main__":
    board = Board()
    c=0
    while board.available_places>=0:
        if c%2==0:
            solver = Solver()
            st = time.time()
            col,value = solver.solve(board)
            end = time.time()
            t1 = float(end-st)

            st = time.time()
            col_1, value = solver.solve(board,solver="alphabetapruning")
            end = time.time()
            t2 = float(end-st)

            print(f"Time taken  By Minmax = {t1:.2f}   By AlphaBetaPruning = {t2:.2f}  Column choosed By MinMax = {col} By AlphaBeta Pruning = {col_1} ")
            board.add_piece(col,1.0)

        else:
            print(board)
            col = int(input(("Enter Column: ")))
            board.add_piece(col,2.0)
        c+=1
