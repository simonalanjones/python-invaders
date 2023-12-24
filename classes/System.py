import importlib
import inspect
import os
from classes.Display import Display
from lib.Event_manager import EventManager
from lib.Controller import Controller

## dont forget about callback in controllers
## perhaps pass an notifier callback and register callback as params into controller instancing line 70
## maybe have a callback class and pass a method or object


class System:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = System()
        return cls._instance

    def __init__(self):
        self.display = Display()
        self.event_manager = EventManager.get_instance()
        self.load_controllers()

      # Class-level dictionary to store callbacks
    callbacks = {}

    # Class-level dictionary to store callback names (labels)
    callback_names = {}

    @classmethod
    def register_callback(cls, key, callback, name=None):
        cls.callbacks[key] = callback

        # Store the callback name if provided
        if name:
            cls.callback_names[key] = name

    @classmethod
    def get_callback(cls, key):
        return cls.callbacks.get(key, None)

    @classmethod
    def callback(cls, key):
        callback_function = cls.callbacks.get(key)
        if callback_function is not None:
            return callback_function()
        else:
            # Optionally handle the case where the key is not found
            # print(f"No callback found for key: {key}")
            return None

    @classmethod
    def debug_callbacks(cls):
        print("Callbacks:")
        for key, callback in cls.callbacks.items():
            # Get the callback name from the dictionary, or use the key as a fallback
            name = cls.callback_names.get(key, key)
            print(
                f"{name}: {callback.__name__ if hasattr(callback, '__name__') else callback}"
            )

    def add_listener(self, event_type, listener):
        self.event_manager.add_listener(event_type, listener)

    def remove_listener(self, event_type, listener):
        self.event_manager.remove_listener(event_type, listener)

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
                        # Create an instance of the controller
                        controller_instance = obj()  ### inject notifier here
                        if not hasattr(controller_instance, "rendering_order"):
                            controller_instance.rendering_order = 0

                        self.controllers.append(controller_instance)

                self.controllers.sort(key=lambda controller: controller.rendering_order)

        for controller_instance in self.controllers:
            if hasattr(controller_instance, "game_ready") and callable(
                controller_instance.game_ready
            ):
                controller_instance.game_ready()
