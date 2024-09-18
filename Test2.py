import time

import Solver
from Board import *
import numpy as np
def test_8062(state, player_id):
    board = Board()
    board.load_board(state)
    solver = Solver.Solver(depth=8)
    solver.algorithm = "α-βpruning"
    t = []
    while board.available_places >= 0:
        if player_id % 2 == 0:
            st = time.time()
            col, value = solver.solve(board)
            end = time.time()
            t.append(float(end-st))
            board.add_piece(col, 1.0)
            print(col+1)
        else:

            col = int(input("Enter Column (1-7)"))
            while col>7 or col<1:
                col = int(input("Enter Column (1-7)"))
            board.add_piece(col, 2.0)
        print(board)
        player_id+=1
    c1 = solver.count_fours(board,1)
    c2 = solver.count_fours(board,2)
    return t,c1,c2
def test_8062(state,player_id):
    board = Board()
    board.load_board(state)
    solver = Solver.Solver(depth=8)
    solver.algorithm = "α-βpruning"
    st = time.time()
    col, value = solver.solve(board)
    end = time.time()
    return int(col+1),float(end-st)
if __name__=="__main__":
    test_8062(np.zeros((6,7)),0)