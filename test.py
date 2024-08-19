from Solver import *
from Board import *
import numpy as np


def test_8062(state, player_id):
    board = Board()
    board.load_board(state)
    solver = Solver(depth=8)
    while board.available_places >= 0:
        if player_id % 2 == 0:
            col, value = solver.solve(board, solver="alphabetapruning")
            board.add_piece(col, 1.0)
            print(col)
        else:

            col = int(input(("Enter Column (1-7): ")))
            while col > 7 or col < 1:
                col = int(input(("Enter Column (1-7): ")))
            board.add_piece(col - 1, 2.0)
        print(board)
        player_id+=1


if __name__=="__main__":
    test_8062(np.zeros((6,7)),0)