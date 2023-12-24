from lib.Event_manager import EventManager


class Controller:
    def __init__(self):
        self.event_manager = EventManager.get_instance()

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


# pygame.quit()
