from lib.Controller import Controller

from classes.factories.Bomb_factory import BombFactory
from classes.containers.Bomb_container import BombContainer
from classes.models.Invader import Invader
from classes.models.Bomb import Bomb
import random


class BombController(Controller):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.enabled = False
        self.max_bombs = 2
        self.grace_period = 60

        self.bomb_types = ["plunger", "squiggly", "rolling"]
        self.bomb_factory = BombFactory()
        self.bomb_container = BombContainer()

        self.event_manager.add_listener(
            "play_delay_complete", self.on_play_delay_complete
        )

        self.register_callback("get_bombs", lambda: self.bomb_container.get_bombs())

    def game_ready(self):
        self.get_invaders_callback = self.get_callback("get_invaders")
        self.get_player_callback = self.get_callback("get_player")
        self.get_invaders_clearpath_callback = self.get_callback(
            "get_invaders_with_clear_path"
        )

    def on_play_delay_complete(self, data):
        self.enabled = True

    def update(self, events, dt):
        invaders = self.get_invaders_callback()
        if len(invaders) > 0 and self.enabled == True:
            # create a new bomb
            if len(self.bomb_container.get_bombs()) < self.max_bombs:
                bomb = self.create_bomb()
                if isinstance(bomb, Bomb):
                    self.bomb_container.add(bomb)

        # Update all existing bomb sprites in this container
        self.counter += 1
        if self.counter == 3:
            self.counter = 0
            for sprite in self.bomb_container:
                sprite.update()
        return self.bomb_container

    def create_bomb(self):
        def get_next_bomb_type():
            if self.bomb_container.has_rolling_shot():
                bomb_type = random.choice(self.bomb_types[:2])
            else:
                bomb_type = random.choice(self.bomb_types)

            bomb_type = self.bomb_types[1]
            return bomb_type

        bomb_type = get_next_bomb_type()
        invader = self.find_attacking_invader(bomb_type)
        if isinstance(invader, Invader):
            return self.bomb_factory.create_bomb(invader, bomb_type)

    def find_attacking_invader(self, bomb_type):
        invaders_with_clear_path = self.get_invaders_clearpath_callback()

        def is_valid_target(invader):
            return invader.active

        def is_rolling_bomb():
            return bomb_type == "rolling" and self.get_player_callback is not None

        if is_rolling_bomb():
            player_rect = self.get_player_callback().get_rect()
            valid_invaders = [
                invader
                for invader in invaders_with_clear_path
                if player_rect.x <= (invader.rect.x + 8) <= (player_rect.x + 16)
                and is_valid_target(invader)
            ]
            if valid_invaders:
                return random.choice(valid_invaders)
        else:
            if invaders_with_clear_path:
                return random.choice(invaders_with_clear_path)

        # Return None if no valid invader is found
        return None
