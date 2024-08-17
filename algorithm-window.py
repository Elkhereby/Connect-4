import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 300
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

# Button properties
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR = (0, 255, 0)
HOVER_COLOR = (255, 0, 0)
BUTTON_FONT = pygame.font.Font(None, 30)
BUTTON_TEXTS = ["Minimax", "Alpha-beta Pruning", "Expectimax"]

# Position buttons vertically under each other
BUTTON_POSITION = [
    (100, 50),
    (100, 120),
    (100, 190)
]

def draw_button(screen, position, text, button_color):
    rect = pygame.Rect(position, (BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, button_color, rect)
    text_surface = BUTTON_FONT.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

running = True

while running:
    screen.fill((0, 0, 0))

    for i, pos in enumerate(BUTTON_POSITION):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect(pos, (BUTTON_WIDTH, BUTTON_HEIGHT)).collidepoint(mouse_pos):
            color = HOVER_COLOR
        else:
            color = BUTTON_COLOR
        draw_button(screen, pos, BUTTON_TEXTS[i], color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, pos in enumerate(BUTTON_POSITION):
                if pygame.Rect(pos, (BUTTON_WIDTH, BUTTON_HEIGHT)).collidepoint(mouse_pos):
                    print(f"{BUTTON_TEXTS[i]} button clicked")

    pygame.display.flip()

pygame.quit()
sys.exit()
