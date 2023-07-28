from classes.player.Player_missile import PlayerMissile
import pygame


class PlayerMissileController:
    def __init__(self, get_invaders_callback, destroy_invader_callback):
        self.player_missile = None
        self.get_invaders_callback = get_invaders_callback
        self.destroy_invader_callback = destroy_invader_callback

    def launch_missile(self, player_rect):
        if self.player_missile == None:
            self.player_missile = PlayerMissile(
                player_rect, self.destroy_player_missile
            )

    def check_collisions(self):
        invaders = self.get_invaders_callback
        collided_invaders = pygame.sprite.spritecollide(
            self.player_missile, invaders(), False
        )
        if collided_invaders:
            collided_invader = collided_invaders[0]
            self.destroy_invader_callback(collided_invader)
            self.player_missile = None

    def update(self):
        self.check_collisions()
        if self.player_missile:
            self.player_missile.rect.y -= 5  # Move the missile vertically upwards
            if self.player_missile.rect.y <= 0:
                self.player_missile = None
            return self.player_missile

    def destroy_player_missile(self):
        self.player_missile = None

    def get_player_missile(self):
        if self.player_missile != None:
            return self.player_missile
