import os
from classes.Controller import Controller
from classes.player.Player_missile import PlayerMissile
import pygame


class PlayerMissileController(Controller):
    def __init__(self):
        super().__init__([])
        self.player_missile = None
        self.ready_flag = False

        # callbacks
        self.get_invaders_callback = None
        self.get_shields_callback = None
        self.get_player_callback = None

    def on_collision(self, data):
        print(data)
        # self.ready_flag = False
        self.player_missile = None

    def on_missile_ready(self, data):
        self.ready_flag = True

    def on_fire_pressed(self, data):
        if self.player_missile == None and self.ready_flag:
            self.player_missile = PlayerMissile(self.get_player_callback().rect)

    def check_collisions(self):
        if self.get_invaders_callback:
            collided_invaders = pygame.sprite.spritecollide(
                self.player_missile, self.get_invaders_callback(), False
            )

            if collided_invaders:
                self.event_manager.notify("invader_hit", collided_invaders[0])
                self.player_missile = None
                self.ready_flag = False

    def update(self, events):
        if self.player_missile:
            self.check_collisions()
            if self.player_missile:
                self.player_missile.rect.y -= 5  # Move the missile vertically upwards
                if self.player_missile.rect.y <= 0:
                    self.player_missile = None
                    self.event_manager.notify("missile_exited")
                return self.player_missile

    def destroy_player_missile(self):
        self.player_missile = None
        self.ready_flag = True

    # shields need access to player missile
    def get_player_missile(self):
        if self.player_missile != None:
            return self.player_missile
