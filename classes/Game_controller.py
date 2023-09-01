import pygame

from classes.Controller import Controller
from classes.invader.Invader_controller import InvaderController
from classes.bomb.Bomb_controller import BombController
from classes.player.Player import Player
from classes.player.Player_controller import PlayerController
from classes.player.Player_missile_controller import PlayerMissileController
from classes.shield.Shield_controller import ShieldController
from classes.player.Player_missile import PlayerMissile
from classes.Baseline_controller import BaselineController
from classes.Input_controller import InputController
from classes.Scoreboard_controller import ScoreboardController
from classes.UI_controller import UIController
from classes.mothership.Mothership_controller import MothershipController
from classes.Audio_controller import AudioController


class GameController(Controller):
    def __init__(self, config):
        super().__init__(config)
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
        self.max_fps = config.get("max_fps")

        self.setup_controllers(config)
        self.setup_controller_callbacks()
        self.setup_game_events()

    def setup_controllers(self, config):
        self.controllers = {
            "invader": InvaderController(config),
            "mothership": MothershipController(config),
            "player": PlayerController(config),
            "shield": ShieldController(config),
            "missile": PlayerMissileController(),
            "bomb": BombController(config),
            "baseline": BaselineController(),
            "input": InputController(config),
            "score": ScoreboardController(config),
            "ui": UIController(config),
            "audio": AudioController(config),
        }

    def setup_controller_callbacks(self):
        self.controllers["baseline"].get_bombs_callback = self.controllers[
            "bomb"
        ].get_bombs

        self.controllers["bomb"].get_invaders_callback = self.controllers[
            "invader"
        ].get_invaders

        self.controllers["bomb"].get_player_callback = self.controllers[
            "player"
        ].get_player

        self.controllers["shield"].get_bombs_callback = self.controllers[
            "bomb"
        ].get_bombs

        self.controllers["shield"].get_missile_callback = self.controllers[
            "missile"
        ].get_player_missile

        self.controllers["shield"].get_invaders_callback = self.controllers[
            "invader"
        ].get_invaders

        self.controllers["missile"].get_player_callback = self.controllers[
            "player"
        ].get_player

        self.controllers["missile"].get_invaders_callback = self.controllers[
            "invader"
        ].get_invaders

        self.controllers["ui"].get_score_callback = self.controllers["score"].get_score

        self.controllers["mothership"].get_score_text_callback = self.controllers[
            "ui"
        ].create_text_surface

        self.controllers["mothership"].get_invader_count_callback = self.controllers[
            "invader"
        ].get_invader_count

        self.controllers["mothership"].get_lowest_invader_y_callback = self.controllers[
            "invader"
        ].get_lowest_invader_y

        self.controllers["mothership"].get_missile_callback = self.controllers[
            "missile"
        ].get_player_missile

    def setup_game_events(self):
        self.event_manager.add_listener("swarm_complete", self.on_swarm_complete)

        self.event_manager.add_listener(
            "mothership_spawned", self.controllers["audio"].on_mothership_spawned
        )

        self.event_manager.add_listener(
            "mothership_hit", self.controllers["audio"].on_mothership_bonus
        )

        self.event_manager.add_listener(
            "mothership_exit", self.controllers["audio"].on_mothership_exit
        )

        self.event_manager.add_listener(
            "points_awarded", self.controllers["score"].on_points_awarded
        )

        self.event_manager.add_listener(
            "invader_hit", self.controllers["invader"].on_invader_hit
        )
        self.event_manager.add_listener(
            "invader_removed", self.controllers["missile"].on_missile_ready
        )

        self.event_manager.add_listener(
            "play_delay_complete", self.controllers["player"].on_play_delay_complete
        )

        self.event_manager.add_listener(
            "play_delay_complete", self.controllers["missile"].on_missile_ready
        )

        self.event_manager.add_listener(
            "play_delay_complete", self.controllers["bomb"].on_play_delay_complete
        )

        self.event_manager.add_listener(
            "left_button_pressed", self.controllers["player"].on_move_left
        )
        self.event_manager.add_listener(
            "left_button_released", self.controllers["player"].on_move_left_exit
        )
        self.event_manager.add_listener(
            "right_button_pressed", self.controllers["player"].on_move_right
        )
        self.event_manager.add_listener(
            "right_button_released", self.controllers["player"].on_move_right_exit
        )

        self.event_manager.add_listener(
            "fire_button_pressed", self.controllers["missile"].on_fire_pressed
        )

        self.event_manager.add_listener(
            "fire_button_pressed", self.controllers["mothership"].on_update_shot_counter
        )

        self.event_manager.add_listener(
            "f1_button_pressed", self.controllers["invader"].on_f1_pressed
        )

    def on_swarm_complete(self, data):
        self.invader_swarm_complete = True

    def launch_player_missile(self, player_rect):
        self.player_missile = PlayerMissile(player_rect)

    def player_missile_remove(self):
        self.player_missile = None

    def update(self, events, dt):
        clock = pygame.time.Clock()

        if self.play_delay_count > 0:
            self.play_delay_count -= 1
            if self.play_delay_count <= 0:
                self.event_manager.notify("play_delay_complete")

        # create a new game surface each frame
        game_surface = pygame.Surface(self.original_screen_size, pygame.SRCALPHA)

        for controller in self.controllers.values():
            if hasattr(controller, "update"):
                canvas_item = controller.update(events, dt)
                # print(canvas_item)
            if hasattr(canvas_item, "draw"):
                canvas_item.draw(game_surface)

        # render the playing surface onto the main window
        self.window_surface.blit(self.scaled_image, self.top_left)
        # scale the playing surface up to target size on main window
        self.window_surface.blit(
            pygame.transform.scale(game_surface, self.larger_screen_size),
            self.top_left,
        )

        pygame.display.flip()
        clock.tick(self.max_fps)
