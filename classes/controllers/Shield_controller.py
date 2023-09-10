from lib.Controller import Controller
from classes.shield.Shield_factory import ShieldFactory
import pygame


class ShieldController(Controller):
    def __init__(self):
        super().__init__()

        shield_factory = ShieldFactory()
        self.rendering_order = -1
        self.shield_container = shield_factory.create_shields()

        self.missile_image_2x = pygame.image.load(
            "sprites/player/player-shot-double-height.png"
        )

    def update(self, events, dt):
        self.check_bomb_collisions()
        self.check_invader_collision()
        self.check_missile_collision()
        return self.shield_container

    def check_missile_collision(self):
        missile_callback = self.get_callback("get_player_missile")
        missile = missile_callback()

        if missile is not None and missile.active:
            _missile = pygame.sprite.Sprite()  # Create an instance of the Sprite class
            _missile.rect = missile.rect.copy()  # Copy the rectangle
            # because the missile moves up 4 pixels each cycle
            # we need a sprite 2x height to ensure that sprite collision
            # doesn't miss any pixels between position jumps
            _missile.image = self.missile_image_2x  # Copy the image
            # _missile.rect.y -= 1  # Adjust the copied missile's position

            for shield_sprite in self.shield_container:
                if pygame.sprite.collide_mask(shield_sprite, _missile):
                    missile.explode(missile.rect.move(-4, -3))
                    # self.rect.x -= 4
                    # self.rect.y -= 3

                    shield_sprite.missile_damage(missile)
                    # self.event_manager.notify("missile_collision", shield_sprite)

    def check_invader_collision(self):
        invader_callback = self.get_callback("get_invaders")
        invaders = invader_callback()
        if invaders:
            collisions = pygame.sprite.groupcollide(
                self.shield_container, invaders, False, False
            )
            for shield_sprite, collided_invaders in collisions.items():
                for invader in collided_invaders:
                    shield_sprite.invader_damage(invader)

    def check_bomb_collisions(self):
        bomb_callback = self.get_callback("get_bombs")
        bomb_sprites = bomb_callback()

        if bomb_sprites is not None:
            for shield_sprite in self.shield_container:
                for bomb_sprite in bomb_sprites:
                    if bomb_sprite.active and pygame.sprite.collide_mask(
                        shield_sprite, bomb_sprite
                    ):
                        bomb_sprite.explode()
                        shield_sprite.bomb_damage(bomb_sprite)

        # if self.get_bombs_callback:
        #     bomb_sprites = self.get_bombs_callback()
        #     if len(bomb_sprites) > 0:
        #         for shield_sprite in self.shield_container:
        #             for bomb_sprite in bomb_sprites:
        #                 collision = pygame.sprite.collide_mask(
        #                     shield_sprite, bomb_sprite
        #                 )

        #                 if collision and bomb_sprite.active:
        #                     bomb_sprite.explode()
        #                     shield_sprite.bomb_damage(bomb_sprite)

        # #x, y = collision
        # global_position = bomb_sprite.rect.topleft

        # # Convert global position to local position inside the shield
        # local_position = (
        #     global_position[0] - shield_sprite.rect.x,
        #     global_position[1] - shield_sprite.rect.y,
        # )
        # # print(local_position)

        # bomb_type = bomb_sprite.bomb_type
        # if bomb_type == "plunger":
        #     y_adjust = -4
        # else:
        #     y_adjust = 4

        # modified_shield_surface = shield_sprite.image.copy()
        # modified_shield_surface.blit(
        #     bomb_sprite.explode_frame,
        #     (local_position[0], y - y_adjust),
        #     special_flags=pygame.BLEND_RGBA_SUB,
        # )
        # shield_sprite.image = modified_shield_surface
        # shield_sprite.mask = pygame.mask.from_surface(
        #     modified_shield_surface
        # )

        # self.bomb_callback(bomb_sprite)
        # bomb_sprite.kill()
