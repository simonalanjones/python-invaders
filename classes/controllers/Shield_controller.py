from lib.Controller import Controller
from classes.factories.Shield_factory import ShieldFactory
from lib.Sprite_sheet import PlayerSpriteSheet
import pygame


class ShieldController(Controller):
    def __init__(self):
        super().__init__()
        self.rendering_order = -1
        self.shield_container = ShieldFactory().create_shields()

    # place any code here that should run when controllers have loaded
    def game_ready(self):
        return

    def update(self, events, dt):
        self.check_bomb_collisions()
        self.check_invader_collision()
        self.check_missile_collision()
        return self.shield_container

    def check_missile_collision(self):
        missile = self.callback("get_player_missile")

        if missile is not None and missile.active:
            for shield_sprite in self.shield_container:
                collision_area = pygame.sprite.collide_mask(shield_sprite, missile)
                if collision_area is not None:
                    shield_sprite.missile_collision(collision_area)
                    missile.explode((-4, 2))

    def check_invader_collision(self):
        invaders = self.callback("get_invaders")
        if invaders:
            collisions = pygame.sprite.groupcollide(
                self.shield_container, invaders, False, False
            )
            for shield_sprite, collided_invaders in collisions.items():
                for invader in collided_invaders:
                    shield_sprite.invader_damage(invader)

    def check_bomb_collisions(self):
        bomb_sprites = self.callback("get_bombs")

        if bomb_sprites is not None:
            for shield_sprite in self.shield_container:
                for bomb_sprite in bomb_sprites:
                    if bomb_sprite.active and pygame.sprite.collide_mask(
                        shield_sprite, bomb_sprite
                    ):
                        bomb_sprite.explode()
                        shield_sprite.bomb_collision(bomb_sprite)

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
