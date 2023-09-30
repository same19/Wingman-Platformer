"""---start of ChatGPT generated code block---"""
"""This file was edited by both ChatGPT and human authors"""
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400  # Adjusted height to 400 pixels
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
HIGHLIGHT_BLUE = (0, 100, 255)
FONT = pygame.font.Font(None, 36)
CORNER_RADIUS = 10

# List of levels and their completion status (True for completed, False for not completed)
sample_levels_completed = [True, False]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level Select")

def draw_rounded_rect(surface, color, rect, radius):
    """
    Draw a rounded rectangle on the given surface.
    """
    x, y, width, height = rect
    pygame.draw.rect(surface, color, (x + radius, y, width - 2 * radius, height))
    pygame.draw.rect(surface, color, (x, y + radius, width, height - 2 * radius))

    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius)

def draw_level_buttons(levels_completed, hover_index):
    button_width = 150
    button_height = 50
    gap = 20
    x = (SCREEN_WIDTH - (button_width + gap) * len(levels_completed)) // 2
    y = (SCREEN_HEIGHT - button_height) // 2  # Centered vertically

    for i, completed in enumerate(levels_completed):
        button_rect = pygame.Rect(x, y, button_width, button_height)
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            hover_index = i
        else:
            hover_index = -1

        if i == hover_index:
            draw_rounded_rect(screen, HIGHLIGHT_BLUE, button_rect, CORNER_RADIUS)
        else:
            draw_rounded_rect(screen, BLUE if completed else GRAY, button_rect, CORNER_RADIUS)
        text = FONT.render(f"Level {i + 1}", True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        x += button_width + gap

    return hover_index

def level_select_screen(levels_completed):
    hover_index = -1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    button_width = 150
                    button_height = 50
                    gap = 20
                    start_x = (SCREEN_WIDTH - (button_width + gap) * len(levels_completed)) // 2
                    for i in range(len(levels_completed)):
                        button_rect = pygame.Rect(start_x, (SCREEN_HEIGHT - button_height) // 2, button_width, button_height)
                        if button_rect.collidepoint(x, y):
                            return i
                            # You can add your level loading logic here
                        start_x += button_width + gap

        screen.fill(SKY_BLUE)
        hover_index = draw_level_buttons(levels_completed, hover_index)
        pygame.display.flip()
    return -1

if __name__ == "__main__":
    level_select_screen(sample_levels_completed)

'''
Base ChatGPT Prompt:
    Make a pygame level select based on a list levels_completed of True and False values. Each level should be highlighted according to its completion status, and all levels should be clickable to play them.
'''