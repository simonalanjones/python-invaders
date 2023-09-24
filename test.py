import pygame


class SpriteSheet:
    def __init__(self, image_path):
        self.sprite_sheet = pygame.image.load(image_path)
        self.sprite_lookup = {}

    def add_sprite(self, name, x, y, width, height):
        self.sprite_lookup[name] = (x, y, width, height)

    def get_sprite(self, name):
        sprite_rect = self.sprite_lookup.get(name)
        if sprite_rect:
            x, y, width, height = sprite_rect
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
            return sprite
        else:
            raise ValueError(f"Sprite with name '{name}' not found in the spritesheet.")


# Example usage:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    # Create a SpriteSheet instance
    sprite_sheet = SpriteSheet("images/font_spritesheet.png")

    # Add sprites to the sprite lookup table with their respective positions and sizes
    sprite_sheet.add_sprite("sprite1", 1, 1, 8, 8)
    sprite_sheet.add_sprite("sprite2", 11, 1, 8, 8)
    sprite_sheet.add_sprite("sprite3", 21, 1, 8, 8)
    # Add more sprites as needed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        sprite = sprite_sheet.get_sprite("sprite1")
        screen.blit(sprite, (100, 100))
        sprite = sprite_sheet.get_sprite("sprite2")
        screen.blit(sprite, (64, 100))
        pygame.display.flip()

    pygame.quit()


# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Define the screen dimensions
# screen_width = 224
# screen_height = 256
# screen = pygame.display.set_mode((screen_width, screen_height))

# # Define the colors based on your provided areas
# colors = [
#     (255, 255, 255),  # White
#     (255, 0, 0),  # Red
#     (255, 255, 255),  # White
#     (0, 255, 0),  # Green
#     (255, 255, 255),  # White
#     (0, 255, 0),  # Green
#     (255, 255, 255),  # White
# ]

# # Define the positions and sizes of the areas
# areas = [
#     {"position": (0, 0), "size": (224, 32)},
#     {"position": (0, 32), "size": (224, 32)},
#     {"position": (0, 64), "size": (224, 120)},
#     {"position": (0, 184), "size": (224, 56)},
#     {"position": (0, 240), "size": (24, 16)},
#     {"position": (24, 240), "size": (112, 16)},
#     {"position": (136, 240), "size": (88, 16)},
# ]

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Fill the screen with the specified colors
#     for i, area in enumerate(areas):
#         color = colors[i]
#         pygame.draw.rect(screen, color, pygame.Rect(area["position"], area["size"]))

#     pygame.display.flip()

# # Quit Pygame
# pygame.quit()
# sys.exit()

# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Define the screen dimensions
# screen_width = 224
# screen_height = 256
# screen = pygame.display.set_mode((screen_width, screen_height))


# # Define the colors based on your provided areas with reduced alpha value (transparency)
# colors = [
#     (255, 255, 255),  # White
#     (255, 0, 0),  # Red
#     (255, 255, 255),  # White
#     (0, 255, 0),  # Green
#     (255, 255, 255),  # White
#     (0, 255, 0),  # Green
#     (255, 255, 255),  # White
# ]

# # Define the alpha values for the colors
# alpha_values = [255, 100, 255, 100, 255, 100, 255]

# # Create semi-transparent surfaces for the colored rectangles
# colored_rect_surfaces = [
#     pygame.Surface((224, 32), pygame.SRCALPHA),
#     pygame.Surface((224, 32), pygame.SRCALPHA),
#     pygame.Surface((224, 120), pygame.SRCALPHA),
#     pygame.Surface((224, 56), pygame.SRCALPHA),
#     pygame.Surface((24, 16), pygame.SRCALPHA),
#     pygame.Surface((112, 16), pygame.SRCALPHA),
#     pygame.Surface((88, 16), pygame.SRCALPHA),
# ]

# # Define the positions and sizes of the areas
# areas = [
#     {"position": (0, 0), "size": (224, 32)},
#     {"position": (0, 32), "size": (224, 32)},
#     {"position": (0, 64), "size": (224, 120)},
#     {"position": (0, 184), "size": (224, 56)},
#     {"position": (0, 240), "size": (24, 16)},
#     {"position": (24, 240), "size": (112, 16)},
#     {"position": (136, 240), "size": (88, 16)},
# ]

# # Fill the colored rectangles with the specified colors and alpha values
# for i, surface in enumerate(colored_rect_surfaces):
#     color = colors[i]
#     alpha = alpha_values[i]
#     # surface.fill((color[0], color[1], color[2], alpha))


# # Create a sprite class
# class PlayerSprite(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
#         self.rect = self.image.get_rect()
#         self.rect.center = (screen_width // 2, screen_height // 2)
#         self.color = (255, 255, 255)
#         self.alpha = 255

#     def modify_pixel_colors(self):
#         area_colors = [0, 1, 0, 3, 0, 3, 0]  # Corresponding colors for each area
#         # for frame in self.modified_frames:
#         for y in range(self.image.get_height()):
#             for x in range(self.image.get_width()):
#                 pixel_color = self.image.get_at((x, y))
#                 pixel_x, pixel_y = (
#                     self.rect.x + x,
#                     self.rect.y + y,
#                 )  # Pixel position in the sprite's coordinate system

#                 for i, area in enumerate(areas):
#                     area_rect = pygame.Rect(area["position"], area["size"])
#                     if area_rect.collidepoint(pixel_x, pixel_y):
#                         color_index = area_colors[i]
#                         new_color = colors[color_index]
#                         pixel_color.r, pixel_color.g, pixel_color.b = new_color
#                         pixel_color.a = 127

#                 self.image.set_at((x, y), pixel_color)

#     def update_color(self):
#         for i, area in enumerate(areas):
#             area_rect = pygame.Rect(area["position"], area["size"])
#             if area_rect.colliderect(self.rect):
#                 self.color, self.alpha = colors[i], alpha_values[i]
#                 return
#         self.color, self.alpha = (0, 0, 0), 255  # Default color (black with full alpha)

#     def update(self):
#         self.modify_pixel_colors()


# # Create a sprite group
# all_sprites = pygame.sprite.Group()
# player_sprite = PlayerSprite()
# all_sprites.add(player_sprite)

# # Set the desired frame rate (60 fps)
# clock = pygame.time.Clock()
# desired_fps = 60

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Check for key presses to move the sprite
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#         player_sprite.rect.x -= 1
#     if keys[pygame.K_RIGHT]:
#         player_sprite.rect.x += 1
#     if keys[pygame.K_UP]:
#         player_sprite.rect.y -= 1
#     if keys[pygame.K_DOWN]:
#         player_sprite.rect.y += 1

#     # Clear the screen
#     screen.fill((0, 0, 0))  # Fill the entire screen with white

#     # Draw the semi-transparent colored rectangles
#     for i, area in enumerate(areas):
#         surface = colored_rect_surfaces[i]
#         screen.blit(surface, (area["position"][0], area["position"][1]))

#     # Update and draw the player sprite
#     all_sprites.update()
#     all_sprites.draw(screen)

#     pygame.display.flip()

#     # Limit the frame rate to desired_fps (60 fps)
#     clock.tick(desired_fps)

# # Quit Pygame
# pygame.quit()
# sys.exit()
