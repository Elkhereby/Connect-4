from solver import *
from Board import *

def test_8062(board_state, player_id):
    if player_id == 1:
        opponent = 2
    else:
        opponent = 1
    board = Board(board_state)
    solver = Solver(depth=8,Ai_piece=player_id,player_piece=opponent)
    col, _ = solver.solve(board, "alphabetapruning")
    return col


if __name__=="__main__":

    board = Board()
    print(board.current_state, '\n')
    player_id = 1
    turn = player_id

    while board.available_places >= 0:
        if turn != player_id:
            solver2 = Solver(depth=8, Ai_piece=2, player_piece=1)
            col, _ = solver2.solve(board, "alphabetapruning")
            board.add_piece(col, 2)
        else:
            col = test_8062(board, player_id)
            board.add_piece(col, player_id)
        print(board.current_state, '\n')
        turn += 1
        turn = turn % 2


