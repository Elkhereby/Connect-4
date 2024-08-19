import random
import sys
import numpy as np
import pygame
from Solver import *
from Board import *

pygame.init()

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0,255,0)
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
COLUMN_COUNT = 7
ROW_COUNT = 6
turn = random.choice([0, 1])


def probabilistic_column_selection(col):#----------------> check empty

    if col == 0:  # Left edge
        probability_distribution = [0.6, 0.4]
        columns = [col, col + 1]
    elif col == COLUMN_COUNT - 1:  # Right edge
        probability_distribution = [0.4, 0.6]
        columns = [col - 1, col]
    else:
        probability_distribution = [0.2, 0.6, 0.2]
        columns = [col - 1, col, col + 1]

    selected_col = random.choices(columns, probability_distribution)[0]

    return selected_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(((ROW_COUNT-1)-r) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(((ROW_COUNT-1)-r) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()





width = SQUARE_SIZE * COLUMN_COUNT
height = SQUARE_SIZE * (ROW_COUNT + 1)

size = (width, height)
algorithm = "alphabetapruning"
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)

board = Board()

game_over = False

solver = Solver()

# Draw the initial empty board
draw_board(board.current_state)
print(turn)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED if turn % 2 == 0 else YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            col = int(posx / SQUARE_SIZE)
            if algorithm.lower()=="ExpectMiniMax":
                col = probabilistic_column_selection(col)
            if board.first_empty_tile(col) is not None:
                if turn % 2 == 0:
                    if not game_over:
                        board.add_piece(col, 2.0)  # Human player (RED)
                        print("Human",turn)
                        pygame.display.update()
                        pygame.time.delay(20)
                        turn += 1  # Change the turn after a valid move

                draw_board(board.current_state)

                # Check for game-over condition here if needed


                #pygame.display.update()
        if not board.available_places:
          game_over = True
        if game_over:
            myfont = pygame.font.SysFont("monospace", 55)
            red_score = solver.count_fours(board.current_state, 2.0)
            yellow_score = solver.count_fours(board.current_state, 1.0)

            # Determine the winner
            if red_score > yellow_score:
                winner_text = "Red Wins!"
                color = RED
            elif yellow_score > red_score:
                winner_text = "Yellow Wins!"
                color=YELLOW
            else:
                winner_text = "It's a Draw!"
                color = WHITE

            # Display the Game Over screen
            screen.fill(BLACK)
            game_over_font = pygame.font.SysFont("monospace", 75)
            game_over_text = game_over_font.render("GAME OVER", True, GREEN)
            winner_text_render = myfont.render(winner_text, True, color)
            score_text_render = myfont.render(f"Red: {red_score} - Yellow: {yellow_score}", True, color)
            game_over_text_rect = game_over_text.get_rect(center=(width / 2, height / 2 - 100))
            winner_text_rect = winner_text_render.get_rect(center=(width / 2, height / 2))
            score_text_rect = score_text_render.get_rect(center=(width / 2, height / 2 + 100))

            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(winner_text_render, winner_text_rect)
            screen.blit(score_text_render, score_text_rect)

            pygame.display.update()

        if turn % 2 != 0:
            if not game_over:
                col, _ = solver.solve(board, algorithm)
                board.add_piece(col, 1.0)  # AI player (YELLOW)
                draw_board(board.current_state)
                print("Ai",turn)
                turn+=1