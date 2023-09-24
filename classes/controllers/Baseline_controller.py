import pygame, os
from lib.Controller import Controller


class BaselineController(Controller):
    def __init__(self):
        self.baselineSprite = pygame.sprite.Sprite()

        # create the surface for the sprite
        self.baselineSprite.image = pygame.Surface((224, 1), pygame.SRCALPHA)
        # define the green color as (R, G, B) tuple
        self.baselineSprite.image.fill((0, 255, 0))

        # Set the rect of the sprite
        self.baselineSprite.rect = self.baselineSprite.image.get_rect()
        self.baselineSprite.rect.x = 0
        self.baselineSprite.rect.y = 240

    def draw(self, surface):
        # draw the baselineSprite onto the specified surface
        surface.blit(self.baselineSprite.image, self.baselineSprite.rect.topleft)

    def update(self, events, dt):
        bomb_callback = self.get_callback("get_bombs")
        bomb_sprites = bomb_callback()
        if len(bomb_sprites) > 0:
            collisions = pygame.sprite.spritecollide(
                self.baselineSprite, bomb_sprites, False
            )
            if collisions:
                for bomb_collision in collisions:
                    bomb_collision.rect.y = 233
                    bomb_collision.active = False
                    masked_canvas = self.baselineSprite.image.copy()
                    masked_canvas.blit(
                        self.baselineImage,
                        # where to draw on the canvas. here its the x position of the bomb and 0 on the y
                        (bomb_collision.rect.x, 0),
                        special_flags=pygame.BLEND_RGBA_MULT,
                    )
                    self.baselineSprite.image = masked_canvas
                # bomb_collision.kill()

        return self
