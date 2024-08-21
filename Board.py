import time

import numpy as np

class Board:

    def __init__(self,parent=None, rows=6, cols=7):

        if parent:
            self.current_state = parent.current_state.copy()
            self.f = 0
            self.rows = parent.rows
            self.cols = parent.cols
            self.available_places = parent.available_places
        else:
            self.current_state = np.zeros((rows, cols))
            self.f = 0
            self.rows = rows
            self.cols = cols
            self.available_places = int(rows * cols)
    def load_board(self,state):
        if state is not None:
            self.current_state = np.array(state)
            self.rows,self.cols = self.current_state.shape
            self.available_places = (self.current_state==0).sum()

    def __hash__(self):
        return hash(self.current_state.tostring())
    def __eq__(self, other):  # operator overloading in equality and comparison and indexing
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        display_str = ""
        for row in range(self.rows):
            display_str += "| " + " | ".join(str(self.current_state[row][col]) for col in range(self.cols)) + " |\n"
        display_str += "--" * (self.cols * 3 + 1) + "\n"
        display_str += "   " + "     ".join(str(i) for i in range(1,self.cols+1)) + "  \n"
        return display_str
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2  # Assuming 1 is PLAYER_PIECE and 2 is AI_PIECE

        if window.count(piece) == 4:
            score += 1000
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 5
        if window.count(opp_piece) == 4:
            score -= 1000

        return score



    def calculate_score(self, piece):#piece is 1 or 2
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(self.current_state[:, self.cols // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.current_state[r, :])]
            for c in range(self.cols - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.cols):
            col_array = [int(i) for i in list(self.current_state[:, c])]
            for r in range(self.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        ## Score positive sloped diagonal
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.current_state[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        ## Score negative sloped diagonal
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.current_state[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        self.f = score
        return self.f

    def first_empty_tile(self, col):

        for i in range(self.rows-1,-1,-1):

            if self.current_state[i][col] == 0:
                return i
        return None  # No empty tile in this column


    def add_piece(self, col, value):
        row = self.first_empty_tile(col)
        if row is not None:
            self.current_state[row][col] = value
            self.available_places -= 1
            return True
        return False
    def remove_piece(self, col):
        for row in range(self.current_state.shape[0]):
            if self.current_state[row][col] != 0:
                self.current_state[row][col] = 0
                self.available_places += 1
                break
    def is_terminal(self):
        return self.available_places == 0
if __name__=="__main__":

    # Example usage:
    board = Board()
    print(board.available_places)
    board.add_piece(3, 1)
    board.add_piece(3, 2)
    board.add_piece(2, 1)
    board.add_piece(2, 2)
    board.add_piece(1, 1)
    board.add_piece(1, 2)
    board.add_piece(0, 1)
    print(board.available_places)
    print("Board state:")
    st= time.time()
    print(board.current_state)
    end = time.time()
    print(end-st)
