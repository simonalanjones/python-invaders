from classes.shield.Shield_factory import ShieldFactory
import pygame


class ShieldController:
    def __init__(self, config):
        self.shield_container = ShieldFactory(config).create_shields()
        self.explode_bomb_image = pygame.image.load(
            "sprites/invader_bomb/bomb_exploding.png"
        )

        self.bomb_stem_image = pygame.image.load(
            "sprites/invader_bomb/explode-stem.png"
        )

    def bombs_ref(self, callback):
        self.get_bombs = callback

    def get_bombs(self):
        return self.get_bombs()

    def invaders_ref(self, callback):
        self.get_invaders = callback

    def get_invaders(self):
        return self.get_invaders()

    def update(self):
        self.check_bomb_collisions()
        self.check_invader_collision()
        return self.shield_container

    def check_invader_collision(self):
        invaders = self.get_invaders()
        if len(invaders) > 0:
            for shield_sprite in self.shield_container:
                for invader in invaders:
                    collision = pygame.sprite.collide_mask(shield_sprite, invader)
                    if collision:
                        shield_sprite.invader_damage(invader)

    def check_bomb_collisions(self):
        bomb_sprites = self.get_bombs()
        if len(bomb_sprites) > 0:
            for shield_sprite in self.shield_container:
                for bomb_sprite in bomb_sprites:
                    collision = pygame.sprite.collide_mask(shield_sprite, bomb_sprite)

                    if collision and bomb_sprite.active:
                        bomb_sprite.explode()
                        shield_sprite.bomb_damage(bomb_sprite)

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
