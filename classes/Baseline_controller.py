import pygame, os


class BaselineController:
    def __init__(self):
        self.baselineSprite = pygame.sprite.Sprite()

        self.baselineImage = pygame.image.load(
            os.path.join("sprites", "invader_bomb", "bomb_exploding_base.png")
        )

        # create the surface for the sprite
        self.baselineSprite.image = pygame.Surface((224, 1), pygame.SRCALPHA)
        # define the green color as (R, G, B) tuple
        self.baselineSprite.image.fill((0, 255, 0))

        # Set the rect of the sprite
        self.baselineSprite.rect = self.baselineSprite.image.get_rect()
        self.baselineSprite.rect.x = 0
        self.baselineSprite.rect.y = 240
        # self.collision_check = pygame.sprite.spritecollide

    def bombs_ref(self, callback):
        self.get_bombs = callback

    def get_bombs(self):
        return self.get_bombs()

    def draw(self, surface):
        # draw the baselineSprite onto the specified surface
        surface.blit(self.baselineSprite.image, self.baselineSprite.rect.topleft)

    def get_base_row(self, bomb_collision):
        bomb_collision.rect.height - 1
        # masked_canvas.blit(bomb_collision.image, (bomb_collision.rect.x, bottom_row_y), special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        bomb_sprites = self.get_bombs()
        if len(bomb_sprites) > 0:
            collisions = pygame.sprite.spritecollide(
                self.baselineSprite, bomb_sprites, False
            )
            if collisions:
                # print("collision")
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
