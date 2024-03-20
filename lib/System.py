import importlib
import inspect
import os

from lib.Display import Display
from lib.Controller import Controller
from lib.State_machine import StateMachine
from lib.Event_object import Event_object
from lib.Collision_manager import CollisionManager


class System(Event_object):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = System()
        return cls._instance

    def __init__(self):
        super().__init__()

        self.collision_manger = CollisionManager.get_instance()
        self.display = Display()
        self.is_paused = False

        self.load_controllers()
        self.state_machine = StateMachine()

        self.is_wiping = False
        self.wipe_x = 0
        self.wipe_speed = 32
        self.callback_manager.register_callback(
            "begin_wipe_animation", lambda: self.on_begin_wipe()
        )
        self.callback_manager.register_callback(
            "clear_wipe", lambda: self.on_clear_wipe()
        )

        self.event_manager.add_listener("pause_pressed", self.on_pause_pressed)

    def on_pause_pressed(self, data):
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True
        print(self.is_paused)

    def on_begin_wipe(self):
        print("starting wipe...")
        self.is_wiping = True

    def on_clear_wipe(self):
        print("clearing wipe..")
        self.is_wiping = False
        self.wipe_x = 0

    def update(self, events):
        self.collision_manger.run_autorun_groups()
        if self.state_machine.has_valid_state():
            self.state_machine.update(events)

            for controller_instance in self.state_machine.get_state_controllers():
                if self.get_controller(controller_instance):
                    controller = self.get_controller(controller_instance)
                    # print(controller.__class__.__name__)

                    if (
                        controller.__class__.__name__ == "InputController"
                        or not self.is_paused
                    ):
                        # Call the update method if it exists on the controller
                        if hasattr(controller, "update"):
                            controller.update(events)
                        else:
                            print(f"update method not found in: {controller_instance}")

            surfaces = []
            for controller_name in self.state_machine.get_state_controllers():
                if self.get_controller(controller_name):
                    controller = self.get_controller(controller_name)

                    if controller and hasattr(controller, "get_surface"):
                        surface = controller.get_surface()
                        surfaces.append(surface)

            if self.is_wiping == True:
                if self.wipe_x <= 224 * 4:
                    self.wipe_x += self.wipe_speed
                    # print(self.wipe_x)
                else:
                    self.event_manager.notify("wipe_animation_complete")

            self.display.update(surfaces, self.is_wiping, self.wipe_x)

    def get_controller(self, target_controller):
        _controller = next(
            (
                controller
                for controller in self.controllers
                if controller.__class__.__name__.replace("Controller", "")
                == target_controller
            ),
            None,
        )
        return _controller

    def load_controllers(self):
        # Initialise an empty list to store the imported controllers
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
                        # Create an instance of the controller
                        controller_instance = obj()
                        if not hasattr(controller_instance, "rendering_order"):
                            controller_instance.rendering_order = 0

                        self.controllers.append(controller_instance)

                self.controllers.sort(key=lambda controller: controller.rendering_order)

        for controller_instance in self.controllers:
            if hasattr(controller_instance, "game_ready") and callable(
                controller_instance.game_ready
            ):
                controller_instance.game_ready()
