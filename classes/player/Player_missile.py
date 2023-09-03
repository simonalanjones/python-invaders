import os
import pygame.sprite


class PlayerMissile(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()

        self.delay = 1
        sprite_path = "sprites/player/player-shot.png"
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.countdown = 0
        self.active = True
        self.rect = self.image.get_rect()
        self.rect.x = player_rect.x + 8
        self.rect.y = player_rect.y
        self.explode_frame = pygame.image.load(
            os.path.join("sprites", "player", "player-shot-explodes.png")
        )

    def modify_pixel_colors(self):
        green = (0, 255, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)

        for y in range(self.image.get_height()):
            for x in range(self.image.get_width()):
                pixel_color = self.image.get_at((x, y))
                if y + self.rect.y >= 191:
                    pixel_color.r, pixel_color.g, pixel_color.b = white
                elif y + self.rect.y <= 35:
                    pixel_color.r, pixel_color.g, pixel_color.b = red
                else:
                    pixel_color.r, pixel_color.g, pixel_color.b = green

                self.image.set_at((x, y), pixel_color)

    def draw(self, surface):
        self.modify_pixel_colors()
        surface.blit(self.image, self.rect)

    def remove(self):
        self.kill()

    def explode(self, position_rect=None):
        if self.active:
            self.image = self.explode_frame
            if position_rect:
                print("updated rect")
                self.rect.x = position_rect[0]
                self.rect.y = position_rect[1]

            print(self.rect)
            # if position_rect
            # self.rect.x -= 4
            # self.rect.y -= 3
            self.active = False
            self.countdown = 30

    def update(self):
        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown <= 0:
                self.kill()
        else:
            # if self.delay <= 0:
            self.delay = 1
            self.rect.y -= 4  # Move the missile vertically upwards
            if self.rect.y <= 42:
                self.explode(())
        # else:
        #   self.delay -= 1
        return self
