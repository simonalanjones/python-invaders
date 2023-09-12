from lib.Controller import Controller

from classes.bomb.Bomb_factory import BombFactory
from classes.bomb.Bomb_container import BombContainer
from classes.invader.Invader import Invader
from classes.bomb.Bomb import Bomb
import random, pygame, os


class BombController(Controller):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.enabled = False
        self.max_bombs = 1
        self.grace_period = 60

        self.bomb_types = ["plunger", "squiggly", "rolling"]
        self.bomb_factory = BombFactory()
        self.bomb_container = BombContainer()
        self.explode_bomb_image = pygame.image.load(
            os.path.join("sprites", "invader_bomb", "bomb_exploding.png")
        )
        self.event_manager.add_listener(
            "play_delay_complete", self.on_play_delay_complete
        )

        self.register_callback("get_bombs", self.get_bombs)

        # self.get_invaders_callback = self.get_callback("get_invaders")
        # self.get_player_callback = self.get_callback("get_player")

    def get_bombs(self):
        return self.bomb_container.get_bombs()

    def on_play_delay_complete(self, data):
        # print("swarm notify in bomb controller")
        self.enabled = True

    def update(self, events, dt):
        invader_callback = self.get_callback("get_invaders")
        invaders = invader_callback()
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
        if self.bomb_container.has_rolling_shot():
            bomb_type = random.choice(self.bomb_types[:2])
        else:
            bomb_type = random.choice(self.bomb_types)

        bomb_type = self.bomb_types[1]

        invader = self.find_attacking_invader(bomb_type)
        if isinstance(invader, Invader):
            return self.bomb_factory.create_bomb(invader, bomb_type)

    def find_attacking_invader(self, bomb_type):
        invaders_with_clear_path = self.get_callback("get_invaders_with_clear_path")()
        if len(invaders_with_clear_path) > 0:
            if bomb_type == "rolling" and self.get_player_callback:
                player_rect = self.get_player_callback().get_rect()
                for invader in invaders_with_clear_path:
                    x1 = invader.rect.x + 8
                    px1 = player_rect.x
                    px2 = px1 + 16
                    if x1 >= px1 and x1 <= px2 and invader.active == True:
                        return invader
            else:
                return invaders_with_clear_path[
                    random.randint(0, len(invaders_with_clear_path) - 1)
                ]
