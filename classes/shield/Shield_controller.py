from classes.Controller import Controller
from classes.shield.Shield_factory import ShieldFactory
import pygame


class ShieldController(Controller):
    def __init__(self, config):
        super().__init__(config)
        self.shield_container = ShieldFactory(config).create_shields()
        self.explode_bomb_image = pygame.image.load(
            "sprites/invader_bomb/bomb_exploding.png"
        )

        self.bomb_stem_image = pygame.image.load(
            "sprites/invader_bomb/explode-stem.png"
        )

        # callbacks defined in Game_controller
        # if not injected they are still callable
        self.get_bombs_callback = lambda: None
        self.get_invaders_callback = lambda: None
        self.get_missile_callback = lambda: None

    def update(self, events, dt):
        self.check_bomb_collisions()
        self.check_invader_collision()
        self.check_missile_collision()
        return self.shield_container

    def check_missile_collision(self):
        missile = self.get_missile_callback()
        if missile is not None and missile.active:
            for shield_sprite in self.shield_container:
                if pygame.sprite.collide_mask(shield_sprite, missile):
                    missile.explode()
                    shield_sprite.missile_damage(missile)
                    # self.event_manager.notify("missile_collision", shield_sprite)

                    # print("collided missile with shield")

    def check_invader_collision(self):
        invaders = self.get_invaders_callback()
        if invaders:
            collisions = pygame.sprite.groupcollide(
                self.shield_container, invaders, False, False
            )
            for shield_sprite, collided_invaders in collisions.items():
                for invader in collided_invaders:
                    shield_sprite.invader_damage(invader)

    def check_bomb_collisions(self):
        bomb_sprites = self.get_bombs_callback()
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
