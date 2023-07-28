import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        sprite_path = "sprites/player/player-base.png"
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 218
        self.target_pos = self.rect.center

    # used by BombController
    def get_rect(self):
        return self.rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)
