from pygame.locals import *
from lib.Controller import Controller


# could be configured with allowed keys
# across different screens (game/highscore entry etc)
# maybe the init method could have a mode which would define the keys it tracks
# and it could be switched as well as set during config
class InputController(Controller):
    def __init__(self):
        super().__init__()

    def update(self, events, state):
        # self.event_manager.notify("escape_button_pressed")
        # def update(self, events, dt):
        for event in events:
            # print("event", event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # print("escape press in input controller update")
                    self.event_manager.notify("escape_button_pressed")

                if event.key == K_k:  # 'K' key pressed
                    self.event_manager.notify("left_button_pressed")
                elif event.key == K_l:  # 'L' key pressed
                    self.event_manager.notify("right_button_pressed")
                elif event.key == K_SPACE:
                    self.event_manager.notify("fire_button_pressed")

            elif event.type == KEYUP:
                if event.key == K_k:  # 'K' key released
                    self.event_manager.notify("left_button_released")
                elif event.key == K_l:  # 'L' key released
                    self.event_manager.notify("right_button_released")
