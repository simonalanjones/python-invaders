import pygame.sprite
from classes.player.Player import Player


class PlayerMissile(pygame.sprite.Sprite):
    def __init__(self, player_rect, missile_destroy_callback):
        super().__init__()
        self.missile_destroy_callback = missile_destroy_callback

        sprite_path = "sprites/player/player-shot.png"
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = player_rect.x + 8
        self.rect.y = player_rect.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y -= 5  # Move the missile vertically upwards
        if self.rect.y <= 0:
            self.destroy()
        return self

    def destroy(self):
        self.missile_destroy_callback()
