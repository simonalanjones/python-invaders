import pygame
import time

# Initialize Pygame
pygame.init()

# Constants
FPS = 60
WIDTH, HEIGHT = 800, 600

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game loop
running = True
prev_time = time.time()
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 200  # Pixels per second

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate elapsed time
    current_time = time.time()
    elapsed_time = current_time - prev_time
    prev_time = current_time

    # Calculate movement based on time
    keys = pygame.key.get_pressed()
    player_dx = (
        (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed * elapsed_time
    )
    player_dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed * elapsed_time

    # Update player position
    player_x += player_dx
    player_y += player_dy

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw player
    pygame.draw.circle(screen, (255, 255, 255), (int(player_x), int(player_y)), 20)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
