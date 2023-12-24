import importlib
import inspect
import os
import pygame

from lib.Controller import Controller
from classes.config.Game_config import GameConfig

##
## need a state manager system to co-ordinate the screens
## state manager can poll the wipe position before changing state
## state manager can be built into base controller?
##


class GameController(Controller):
    STARTING_LIVES = 1

    def __init__(self):
        super().__init__()
        config = GameConfig()

        # screen wipe settings
        self.wipe_x = 0  # Initial position of the wipe effect
        self.wipe_speed = 32  # Adjust this to control the speed of the wipe
        self.is_wiping = False

        self.lives = self.STARTING_LIVES
        self.has_extra_life = True
        self.play_delay_count = 120
        self.top_left = config.get("top_left")
        self.original_screen_size = config.get("original_screen_size")
        self.larger_screen_size = config.get("larger_screen_size")

        _bg_image = pygame.image.load(config.get_file_path(config.get("bg_image_path")))

        self.scaled_image = pygame.transform.scale(_bg_image, self.larger_screen_size)
        # add , pygame.FULLSCREEN to run without border
        self.window_surface = pygame.display.set_mode(self.larger_screen_size)

        self.event_manager.add_listener(
            "escape_button_pressed", self.on_escape_button_pressed
        )
        self.event_manager.add_listener(
            "player_explosion_complete", self.on_player_explosion_complete
        )

        self.event_manager.add_listener(
            "extra_life_awarded", self.on_extra_life_awarded
        )

        self.event_manager.add_listener("game_over_animation_ended", self.on_begin_wipe)

        self.register_callback("get_lives_count", lambda: self.lives)
        self.register_callback("get_extra_life", lambda: self.has_extra_life)

        # self.event_manager.add_listener("game_over_animation_ended", self.on_restart)

    def on_begin_wipe(self, data):
        print("starting wipe...")
        self.is_wiping = True

    def on_restart(self, data):
        for controller in self.controllers:
            if hasattr(controller, "game_restart") and callable(
                controller.game_restart
            ):
                controller.game_restart()

    def debug_controllers(self):
        print("Ordered Controllers:")
        for controller in self.controllers:
            print(
                f"{controller.__class__.__name__} - Rendering Order: {controller.rendering_order}"
            )

    def load_controllers(self):
        # Initialize an empty list to store the imported controllers
        self.controllers = []

        # Construct the full directory path for controllers
        controllers_directory = os.path.join("classes", "controllers")

        # Loop through files in the controllers directory
        for filename in os.listdir(controllers_directory):
            if filename.endswith("_controller.py") and filename != "game_controller.py":
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
                        # Create an instance of the controller
                        controller_instance = obj()
                        if not hasattr(controller_instance, "rendering_order"):
                            controller_instance.rendering_order = 0

                        self.controllers.append(controller_instance)

                self.controllers.sort(key=lambda controller: controller.rendering_order)

        # when all controllers have loaded, call the game_ready function
        # which is when it is safe to refer between all controllers
        for controller_instance in self.controllers:
            if hasattr(controller_instance, "game_ready") and callable(
                controller_instance.game_ready
            ):
                controller_instance.game_ready()

    def on_extra_life_awarded(self, data):
        self.has_extra_life = False
        self.lives += 1

    def on_escape_button_pressed(self, data):
        pygame.quit()

    def on_player_explosion_complete(self, data):
        self.lives -= 1
        if self.lives > 0:
            self.play_delay_count = 120
        else:
            self.event_manager.notify("game_ended")
            # manage game over here
            return

    def update(self, events, dt):
        if self.play_delay_count > 0:
            self.play_delay_count -= 1
            if self.play_delay_count <= 0:
                self.event_manager.notify("play_delay_complete")

        # create a new game surface each frame
        game_surface = pygame.Surface(self.original_screen_size, pygame.SRCALPHA)
        # game_surface.fill((0, 0, 0))

        ## have an intermediate surface that all controllers get blitted to
        ## have a background surface which gets the background image
        ## have a foreground surface which gets the wipe blitted
        ## then blit all of them onto main window
        ## could just have the wipe render below the score board

        for controller_instance in self.controllers:
            # Call the update method if it exists on the controller
            if hasattr(controller_instance, "update"):
                canvas_item = controller_instance.update(events, dt)
                # Check if the controller returns an object with a "draw" method
                if canvas_item and hasattr(canvas_item, "draw"):
                    canvas_item.draw(game_surface)

        # render the playing surface onto the main window
        # if not self.is_wiping:
        self.window_surface.blit(self.scaled_image, self.top_left)

        # scale the playing surface up to target size on main window
        self.window_surface.blit(
            pygame.transform.scale(game_surface, self.larger_screen_size),
            self.top_left,
        )

        if self.is_wiping:
            if self.wipe_x <= 224 * 4:
                self.window_surface.blit(
                    self.scaled_image, (0, 160), (0, 160, self.wipe_x, 256 * 4)
                )
                self.wipe_x += self.wipe_speed
            else:
                # possibly have a callback to poll the status instead of event callbacks
                self.event_manager.notify("wipe_animation_complete")
                self.is_wiping = False
                self.wipe_x = 0
