import pygame
from lib.Event_manager import EventManager

import importlib
import os
import inspect


class Controller:
    def __init__(self, config):
        self.event_manager = EventManager.get_instance()
        self.config = config

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
        return cls.callbacks.get(key)

    @classmethod
    def debug_callbacks(cls):
        print("Callbacks:")
        for key, callback in cls.callbacks.items():
            # Get the callback name from the dictionary, or use the key as a fallback
            name = cls.callback_names.get(key, key)
            print(
                f"{name}: {callback.__name__ if hasattr(callback, '__name__') else callback}"
            )


pygame.quit()
