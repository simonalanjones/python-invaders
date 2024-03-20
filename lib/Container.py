import pygame
from lib.Event_object import Event_object
from lib.Collision_manager import CollisionManager


# container for multiple sprites in a group such as invader and shields
class Container(pygame.sprite.Group, Event_object):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        Event_object.__init__(self)
        self.collision_manager = CollisionManager.get_instance()


# container for use with single sprite group such as player and player missile
class ContainerSingle(pygame.sprite.GroupSingle, Event_object):
    def __init__(self):
        pygame.sprite.GroupSingle.__init__(self)
        Event_object.__init__(self)
        self.collision_manager = CollisionManager.get_instance()
