import pygame
import sys

# Initialize Pygame
pygame.init()

# Define the screen dimensions
screen_width = 224
screen_height = 256
screen = pygame.display.set_mode((screen_width, screen_height))

# Define the colors based on your provided areas
colors = [
    (255, 255, 255),  # White
    (255, 0, 0),  # Red
    (255, 255, 255),  # White
    (0, 255, 0),  # Green
    (255, 255, 255),  # White
    (0, 255, 0),  # Green
    (255, 255, 255),  # White
]

# Define the positions and sizes of the areas
areas = [
    {"position": (0, 0), "size": (224, 32)},
    {"position": (0, 32), "size": (224, 32)},
    {"position": (0, 64), "size": (224, 120)},
    {"position": (0, 184), "size": (224, 56)},
    {"position": (0, 240), "size": (24, 16)},
    {"position": (24, 240), "size": (112, 16)},
    {"position": (136, 240), "size": (88, 16)},
]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the specified colors
    for i, area in enumerate(areas):
        color = colors[i]
        pygame.draw.rect(screen, color, pygame.Rect(area["position"], area["size"]))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
