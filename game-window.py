import random
import sys
import time

import numpy as np
import pygame
from Solver import *
from Board import *

pygame.init()
pygame.init()

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Game board dimensions
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
COLUMN_COUNT = 7
ROW_COUNT = 6

# Window dimensions
width = SQUARE_SIZE * COLUMN_COUNT
height = SQUARE_SIZE * (ROW_COUNT + 1)

# Button properties
BUTTON_WIDTH, BUTTON_HEIGHT = 180, 50  # Decreased width
BUTTON_COLOR = GREEN
HOVER_COLOR = RED
BUTTON_FONT = pygame.font.Font(None, 30)
BUTTON_TEXTS = ["MinMax", "α-β Pruning", "ExpectMiniMax"]

# Position buttons horizontally beside each other under the board
BUTTON_POSITION = [
    (60, height + 10),
    (270, height + 10),
    (480, height + 10)
]

# Adjusted window size to accommodate buttons
size = (width, height + BUTTON_HEIGHT + 20)
algorithm = "α-β Pruning"
selected_button = None
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)

board = Board()
game_over = False
solver = Solver(depth=8)
turn = random.choice([0,1])

def draw_button(screen, position, text, button_color):
    rect = pygame.Rect(position, (BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, button_color, rect)
    text_surface = BUTTON_FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def probabilistic_column_selection(col):
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
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE / 2) + SQUARE_SIZE), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(((ROW_COUNT - 1) - r) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(((ROW_COUNT - 1) - r) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()

# Draw the initial empty board
draw_board(board.current_state)

# Draw the buttons
for i, text in enumerate(BUTTON_TEXTS):
    draw_button(screen, BUTTON_POSITION[i], text, BUTTON_COLOR)

while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED if turn % 2 == 0 else YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)

                # Handle hover effect for buttons
                for i, pos in enumerate(BUTTON_POSITION):
                    rect = pygame.Rect(pos, (BUTTON_WIDTH, BUTTON_HEIGHT))
                    if rect.collidepoint(mouse_pos):
                        color = HOVER_COLOR if selected_button != i else RED
                        draw_button(screen, pos, BUTTON_TEXTS[i], color)
                    else:
                        color = GREEN if selected_button != i else RED
                        draw_button(screen, pos, BUTTON_TEXTS[i], color)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            posy = event.pos[1]
            col = int(posx / SQUARE_SIZE)
            if posy<=550:
                if algorithm == "Expectimax":
                    col = probabilistic_column_selection(col)
                if board.first_empty_tile(col) is not None:
                    if turn % 2 == 0:
                        if not game_over:
                            board.add_piece(col, 2.0)  # Human player (RED)
                            draw_board(board.current_state)
                            print("Human", turn)
                            pygame.display.update()
                            pygame.time.delay(20)
                            turn += 1  # Change the turn after a valid move

                    draw_board(board.current_state)
            else:
                # Check if a button was clicked
                for i, pos in enumerate(BUTTON_POSITION):
                    rect = pygame.Rect(pos, (BUTTON_WIDTH, BUTTON_HEIGHT))
                    if rect.collidepoint(mouse_pos):
                        selected_button = i
                        algorithm = BUTTON_TEXTS[i].lower()
                        print("algorithm = ",algorithm)

                        break

        pygame.display.update()

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
                color = YELLOW
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
                solver.algorithm = algorithm
                st = time.time()
                col, _ = solver.solve(board)
                end = time.time()

                board.add_piece(col, 1.0)  # AI player (YELLOW)
                draw_board(board.current_state)
                print("AI", col,"Time Taken",str(end-st))
                turn += 1
