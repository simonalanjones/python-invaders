import pygame
from pygame.locals import *
from classes.invader.Invader_controller import InvaderController

from classes.bomb.Bomb_controller import BombController
from classes.player.Player import Player
from classes.player.Player_controller import PlayerController
from classes.player.Player_missile_controller import PlayerMissileController
from classes.shield.Shield_controller import ShieldController
from classes.player.Player_missile import PlayerMissile
from classes.Baseline_controller import BaselineController

clock = pygame.time.Clock()


class GameController:
    def __init__(self, config):
        self.bombs_enabled = False
        self.play_delay_count = 120
        self.player_on_screen = False

        self.player_missile = None
        self.invader_swarm_complete = False
        self.top_left = config.get("top_left")
        self.original_screen_size = config.get("original_screen_size")
        self.larger_screen_size = config.get("larger_screen_size")

        _bg_image = pygame.image.load(config.get_file_path(config.get("bg_image_path")))

        self.scaled_image = pygame.transform.scale(_bg_image, self.larger_screen_size)
        self.window_surface = pygame.display.set_mode(self.larger_screen_size)

        self.invader_controller = InvaderController(config)
        self.shield_controller = ShieldController(config)

        self.player_missile_controller = PlayerMissileController(
            self.invader_controller.get_invaders,
            self.invader_controller.destroy_invader_callback,
        )
        self.player_controller = PlayerController(
            Player(), self.player_missile_controller.launch_missile
        )
        # inject the function that returns the active invaders.
        # the bomb container will need this function before dropping bombs
        self.bomb_controller = BombController(config)
        self.bomb_controller.invaders_ref(self.invader_controller.get_invaders)
        self.bomb_controller.player_ref(self.player_controller.get_player)

        self.shield_controller.bombs_ref(self.bomb_controller.get_bombs)
        self.shield_controller.invaders_ref(self.invader_controller.get_invaders)

        self.invader_controller.pause_player_missile(
            self.player_controller.pause_missile_launch
        )
        self.invader_controller.resume_player_missile(
            self.player_controller.resume_missile_launch
        )
        self.invader_controller.notify_swarm_complete(
            self.callback_notify_swarm_complete
        )

        self.baseline_controller = BaselineController()
        self.baseline_controller.bombs_ref(self.bomb_controller.get_bombs)

        self.max_fps = config.get("max_fps")

    def callback_notify_swarm_complete(self):
        self.invader_swarm_complete = True

    def launch_player_missile(self, player_rect):
        self.player_missile = PlayerMissile(player_rect)

    def player_missile_remove(self):
        self.player_missile = None

    # def handle_player_controls(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[K_LEFT]:
    #         self.player_controller.move_left()
    #     if keys[K_RIGHT]:
    #         self.player_controller.move_right()

    def update(self, events):
        if self.play_delay_count > 0:
            self.play_delay_count -= 1
            if self.play_delay_count <= 0:
                self.bomb_controller.enable_bombs()
                self.player_on_screen = True

        # create a new game surface each frame
        game_surface = pygame.Surface(self.original_screen_size, pygame.SRCALPHA)

        if self.player_on_screen == True:
            self.player_controller.update(events)
            # self.handle_player_controls()
            self.player_controller.get_player().draw(game_surface)

            player_missile = self.player_missile_controller.get_player_missile()
            if player_missile != None:
                player_missile.draw(game_surface)
                self.player_missile_controller.update()

        self.invader_controller.update().draw(game_surface)
        self.shield_controller.update().draw(game_surface)
        self.bomb_controller.update().draw(game_surface)
        self.baseline_controller.update().draw(game_surface)

        # render the playing surface onto the main window
        self.window_surface.blit(self.scaled_image, self.top_left)
        # scale the playing surface up to target size on main window
        self.window_surface.blit(
            pygame.transform.scale(game_surface, self.larger_screen_size),
            self.top_left,
        )

        pygame.display.flip()
        clock.tick(self.max_fps)
