import pygame


class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.original_image = image.convert_alpha()  # Store the original image
        self.image = image.copy()  # Create a copy for modification
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # create the mask from the shield image
        # used in collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def bomb_damage(self, bomb_sprite):
        shield_rect = self.rect
        global_position = bomb_sprite.rect.topleft

        # Convert global position to local position inside the shield
        local_position = (
            global_position[0] - shield_rect.x,
            global_position[1] - shield_rect.y,
        )
        # print(local_position)

        bomb_type = bomb_sprite.bomb_type
        # if bomb_type == "plunger":
        #     y_adjust = -4
        # else:
        #     y_adjust = 2

        y_adjust = 2

        modified_shield_surface = self.image.copy()
        modified_shield_surface.blit(
            bomb_sprite.explode_frame,
            # (local_position[0], 0 - y_adjust),
            (local_position[0], local_position[1]),
            special_flags=pygame.BLEND_RGBA_SUB,
        )
        self.image = modified_shield_surface
        # update the sprite mask so future collisions
        # use the mask rather than a basic rect
        self.mask = pygame.mask.from_surface(modified_shield_surface)

    def invader_damage(self, invader_sprite):
        shield_rect = self.rect
        invader_rect = invader_sprite.rect
        overlap_rect = shield_rect.clip(invader_rect)
        overlap_rect.x -= shield_rect.x
        overlap_rect.y -= shield_rect.y

        overlap_surface = pygame.Surface(overlap_rect.size, pygame.SRCALPHA)
        overlap_surface.fill((255, 255, 255))

        modified_shield_surface = self.image.copy()
        modified_shield_surface.blit(
            overlap_surface,
            overlap_rect,
            special_flags=pygame.BLEND_RGBA_SUB,
        )
        self.image = modified_shield_surface
        self.mask = pygame.mask.from_surface(modified_shield_surface)

    # def remove_collision(self, sprite):
    #     if pygame.sprite.collide_mask(self, sprite):
    #         relative_x = sprite.rect.x - self.rect.x
    #         relative_y = sprite.rect.y - self.rect.y
    #         sprite_mask = pygame.mask.from_surface(sprite.image)

    #         # Create a new mask to store the modified mask without modifying the original mask
    #         modified_mask = self.mask.copy()
    #         modified_mask.erase(sprite_mask, (relative_x, relative_y))

    #         # Create a new surface using the modified mask and preserve transparency
    #         self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
    #         self.image.blit(self.original_image, (0, 0))
    #         self.mask = modified_mask

    #         self.update_image()  # Update the shield image after removing collision

    # def update_image(self):
    #     self.image = pygame.Surface(
    #         self.rect.size, pygame.SRCALPHA
    #     )  # Create a new transparent surface
    #     self.image.blit(
    #         self.original_image, (0, 0)
    #     )  # Blit the original image onto the new surface
    #     mask_surface = (
    #         self.mask.to_surface()
    #     )  # Create a surface representing the modified mask
    #     self.image.blit(
    #         mask_surface, (0, 0)
    #     )  # Blit the modified mask onto the shield image
    #     self.image.set_colorkey((0, 0, 0))  # Set black as the transparent color
