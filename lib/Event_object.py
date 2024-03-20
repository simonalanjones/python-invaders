from lib.Event_manager import EventManager
from lib.Callback_manager import CallbackManager


# a base class that provides event management and callback access
class Event_object:
    def __init__(self):
        self.event_manager = EventManager.get_instance()
        self.callback_manager = CallbackManager.get_instance()
