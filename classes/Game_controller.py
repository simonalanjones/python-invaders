import importlib
import inspect
import os
import pygame
import sys

from lib.Controller import Controller


class GameController(Controller):
    def __init__(self, config):
        super().__init__(config)
        self.bombs_enabled = False
        self.play_delay_count = 120
        self.player_on_screen = False

        self.player_missile = None
        # self.invader_swarm_complete = False
        self.top_left = config.get("top_left")
        self.original_screen_size = config.get("original_screen_size")
        self.larger_screen_size = config.get("larger_screen_size")

        _bg_image = pygame.image.load(config.get_file_path(config.get("bg_image_path")))

        self.scaled_image = pygame.transform.scale(_bg_image, self.larger_screen_size)
        # add , pygame.FULLSCREEN to run without border
        self.window_surface = pygame.display.set_mode(self.larger_screen_size)
        self.max_fps = config.get("max_fps")

        self.event_manager.add_listener(
            "escape_button_pressed", self.on_escape_button_pressed
        )

        self.setup_game_events()

    def debug_controllers(self):
        print("Ordered Controllers:")
        for controller in self.controllers:
            print(
                f"{controller.__class__.__name__} - Rendering Order: {controller.rendering_order}"
            )

    def load_controllers(self, config):
        # Initialize an empty list to store the imported controllers
        self.controllers = []

        # Construct the full directory path for controllers
        controllers_directory = os.path.join("classes", "controllers")

        # Loop through files in the controllers directory
        for filename in os.listdir(controllers_directory):
            if filename.endswith("_controller.py"):
                # Extract the module name without the extension
                module_name = filename[:-3]

                # Construct the full module path
                module_path = f"classes.controllers.{module_name}"

                # Import the module dynamically
                module = importlib.import_module(module_path)

                # Check if the module defines a controller class and add it to the list
                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, Controller)
                        and obj != Controller
                    ):
                        # Create an instance of the controller with the config
                        controller_instance = obj(config)
                        if not hasattr(controller_instance, "rendering_order"):
                            controller_instance.rendering_order = 0

                        self.controllers.append(controller_instance)

                self.controllers.sort(key=lambda controller: controller.rendering_order)

    def setup_game_events(self):
        pass
        # self.event_manager.add_listener("swarm_complete", self.on_swarm_complete)

    def on_escape_button_pressed(self):
        pygame.quit()
        sys.exit()

    def on_swarm_complete(self, data):
        self.invader_swarm_complete = True

    # def launch_player_missile(self, player_rect):
    #     self.player_missile = PlayerMissile(player_rect)

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

        for controller_instance in self.controllers:
            # Call the update method if it exists on the controller
            if hasattr(controller_instance, "update"):
                canvas_item = controller_instance.update(events, dt)
                # Check if the controller returns an object with a "draw" method
                if canvas_item and hasattr(canvas_item, "draw"):
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
