import solver
from Board import *
import numpy as np
import Solver_old
def test_8062(state, player_id):
    board = Board()
    board.load_board(state)
    solver = Solver.Solver(depth=8)
    solver_2 = Solver_old.Solver(depth=8,Ai_piece=2,player_piece=1)
    while board.available_places >= 0:
        if player_id % 2 == 0:
            col, value = solver.solve(board, solver="alphabetapruning")
            board.add_piece(col, 1.0)
            print(col+1)
        else:

            col, value = solver_2.solve(board, solver="alphabetapruning")
            board.add_piece(col, 2.0)
        print(board)
        player_id+=1


if __name__=="__main__":
    test_8062(np.zeros((6,7)),0)