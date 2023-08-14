import os
import pygame.sprite


class PlayerMissile(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()

        sprite_path = "sprites/player/player-shot.png"
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.countdown = 0
        self.active = True
        self.rect = self.image.get_rect()
        self.rect.x = player_rect.x + 8
        self.rect.y = player_rect.y
        self.explode_frame = pygame.image.load(
            os.path.join("sprites", "player", "player-shot-explodes.png")
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def explode(self):
        if self.active:
            self.image = self.explode_frame
            self.rect.x -= 4
            self.active = False
            self.countdown = 30

    def update(self):
        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown <= 0:
                self.kill()
        else:
            self.rect.y -= 5  # Move the missile vertically upwards
            if self.rect.y <= 10:
                self.explode()
        return self
