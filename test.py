from Solver import *
from Board import *
import time
def test_8062(board_state, player_id):
    if player_id == 1:
        opponent = 2
    else:
        opponent = 1
    board = Board()
    board.load_board(board_state)
    solver = Solver(depth=8,Ai_piece=player_id,player_piece=opponent,algorithm="α-β Pruning",draw_tree=False)

    st = time.time()
    col, _ = solver.solve(board)
    end = time.time()
    if col is None:
        return None
    return int(col+1),float(end-st)


if __name__=="__main__":

    board = Board()
    print(board, '\n')
    player_id = 1
    turn = player_id

    while board.available_places >= 0:
        if turn != player_id:
            solver2 = Solver(depth=8, Ai_piece=2, player_piece=1)
            col, _ = solver2.solve(board)
            board.add_piece(col, 2)
        else:
            col,t = test_8062(board.current_state, player_id)
            board.add_piece(col-1, player_id)
        print(board, '\n')
        turn += 1
        turn = turn % 2
        print("turn = ",turn)

