import numpy as np
import random
import math

Human = 1
AI = 2
Empty = 0
Rows = 6
Columns = 7
Depth = 4


class Board:
    def __init__(self):
        self.board = np.zeros((Rows, Columns))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[Rows - 1][col] == 0

    def empty_row(self, col):
        for r in range(Rows):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def check_fours(self, piece):
        count = 0
        for c in range(Columns - 3):  # Check horizontal
            for r in range(Rows):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and \
                        self.board[r][c + 3] == piece:
                    count += 1

        for c in range(Columns):  # Check vertical
            for r in range(Rows - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and \
                        self.board[r + 3][c] == piece:
                    count += 1

        for c in range(Columns - 3):  # Check positive diagonals
            for r in range(Rows - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][
                    c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    count += 1

        for c in range(Columns - 3):  # Check negative diagonals
            for r in range(3, Rows):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][
                    c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    count += 1

        return count

    def get_valid_locations(self):
        valid_locations = []
        for col in range(Columns):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def score_position(self, piece):
        score = 0
        center_array = [int(i) for i in list(self.board[:, Columns // 2])]  # Score for center column
        center_count = center_array.count(piece)
        score += center_count * 2

        for r in range(Rows):  # Score Horizontal
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(Columns - 3):
                play = row_array[c:c + 4]
                score += evaluate_play(play, piece)

        for c in range(Columns):  # Score Verticl
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(Rows - 3):
                play = col_array[r:r + 4]
                score += evaluate_play(play, piece)

        for r in range(Rows - 3):  # Score positive diagonal
            for c in range(Columns - 3):
                play = [self.board[r + i][c + i] for i in range(4)]
                score += evaluate_play(play, piece)

        for r in range(Rows - 3):  # Score negative diagonal
            for c in range(Columns - 3):
                play = [self.board[r + 3 - i][c + i] for i in range(4)]
                score += evaluate_play(play, piece)

        return score

    def is_terminal_node(self):
        return len(self.get_valid_locations()) == 0


def evaluate_play(play, piece):
    score = 0
    opp_piece = Human
    if piece == Human:
        opp_piece = AI

    if play.count(piece) == 4:
        score += 10  # Winning move
    elif play.count(piece) == 3 and play.count(Empty) == 1:
        score += 5  # Strong potential move
    elif play.count(piece) == 2 and play.count(Empty) == 2:
        score += 2  # Moderate potential move

    if play.count(opp_piece) == 3 and play.count(Empty) == 1:
        score -= 4  # Prevent opponent's strong move

    return score


def minimax_without_pruning(board, depth, max):
    valid_locations = board.get_valid_locations()
    is_terminal = board.is_terminal_node()
    if depth == 0 or is_terminal:
        if is_terminal:
            return None, 0
        else:  # Depth is zero
            return None, board.score_position(AI)
    if max:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            b_copy = Board()
            b_copy.board = board.board.copy()
            b_copy.drop_piece(row, col, AI)
            new_score = minimax_without_pruning(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            b_copy = Board()
            b_copy.board = board.board.copy()
            b_copy.drop_piece(row, col, Human)
            new_score = minimax_without_pruning(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def minimax(board, depth, alpha, beta, max):
    valid_locations = board.get_valid_locations()
    is_terminal = board.is_terminal_node()
    if depth == 0 or is_terminal:
        if is_terminal:
            return None, 0
        else:  # Depth is zero
            return None, board.score_position(AI)
    if max:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            b_copy = Board()
            b_copy.board = board.board.copy()
            b_copy.drop_piece(row, col, AI)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            b_copy = Board()
            b_copy.board = board.board.copy()
            b_copy.drop_piece(row, col, Human)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def run_game():
    board = Board()
    board.print_board()
    game_over = False
    turn = int(input("select Who to start 1->Human , 2->AI (1-2):"))
    algo = int(input("select Who to start 1->minimax with pruning , 2->minimax without pruning (1-2):"))

    while not game_over:
        if turn == Human:
            col = int(input("Player 1 Make your Selection (0-6): "))
            if board.is_valid_location(col):
                row = board.empty_row(col)
                board.drop_piece(row, col, Human)

        else:
            if algo == 1:
                col, minimax_score = minimax(board, Depth, -math.inf, math.inf, True)
            else:
                col, minimax_score = minimax_without_pruning(board, Depth, True)

            if board.is_valid_location(col):
                row = board.empty_row(col)
                board.drop_piece(row, col, AI)
        board.print_board()

        print(f"Player 1 Score: {board.check_fours(Human)}")
        print(f"AI Score: {board.check_fours(AI)}")

        if board.is_terminal_node():
            game_over = True
            print("Game Over!")
            print(f"Final Player 1 Score: {board.check_fours(Human)}")
            print(f"Final AI Score: {board.check_fours(AI)}")

        turn += 1
        turn = turn % 2


if __name__ == "__main__":
    run_game()
