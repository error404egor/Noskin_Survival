import typing
from column import Column
import pygame
from consts import Tile_side, Player_x, Player_y, Screen_width, Screen_height


class Lavel:
    def __init__(self,
                 layers: list[pygame.sprite.Group, ...],
                 visible_tiles_types_and_groups: {"0": pygame.sprite.Group, "1": pygame.sprite.Group}):
        self.layers = layers
        self.visible_tiles_types_and_groups = visible_tiles_types_and_groups
        self.spawn_x = self.spawn_x_st = Player_x
        self.spawn_y = self.spawn_y_st = Player_y

    def update(self,
               dif_x: int, dif_y: int):
        for layer in self.layers:
            layer.update(dif_x, dif_y)

    def draw(self,
             screen: pygame.Surface):
        for layer in self.layers:
            layer.draw(screen)

    def set_spawn(self, x: int, y: int):
        self.spawn_x = x
        self.spawn_y = y

    def move_to_spawn(self, x, y):
        left, top = self.layers[0].sprites()[0].rect.topleft
        right, bottom = self.layers[0].sprites()[-1].rect.bottomright
        left_st, top_st = (Screen_width - right + left) // 2, (Screen_width - bottom + top) // 2
        tomove_x = left_st - left + (self.spawn_x - self.spawn_x_st)
        tomove_y = top_st - top + (self.spawn_y - self.spawn_y_st)
        self.update(tomove_x, tomove_y)






class Tile(pygame.sprite.Sprite):
    def __init__(self,
                 x: int, y: int,
                 texture: pygame.Surface,
                 layer_of_tile_group: pygame.sprite.Group,
                 tile_group: pygame.sprite.Group,
                 transparency: str,
                 size: tuple) -> None:
        super().__init__()
        self.image = texture
        self.rect = pygame.rect.Rect(x + (Tile_side - size[0]) // 2, y + (Tile_side - size[1]) // 2, *size)
        self.transparency = transparency
        self.add(layer_of_tile_group, tile_group)

    def update(self, x: int, y: int) -> None:
        self.rect.x -= x
        self.rect.y -= y


class AnimCount:
    def __init__(self, n: int, left_anims: list, right_anims: list, stand_anim: str,
                 count=0, fpu=1, right=True, stand=True) -> None:
        self.n = n
        self.count = count % (n * fpu)
        self.right = right
        self.stand = stand
        self.fpu = fpu
        self.left_anims = left_anims
        self.right_anims = right_anims
        self.stand_anim = stand_anim

    def get_anim(self) -> pygame.Surface:
        if self.stand:
            return self.stand_anim
        elif self.right:
            return self.right_anims[int(self.count // self.fpu)]
        else:
            return self.left_anims[int(self.count // self.fpu)]


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int, vision_range: int,
                 anim: AnimCount, player_group: pygame.sprite.Group) -> None:
        super().__init__()
        self.anim = anim
        self.image = self.anim.get_anim()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.vision_range = vision_range
        player_group.add(self)

    def update(self, opaque_tiles_group: pygame.sprite.Group) -> typing.Tuple[int, int]:
        x_dif, y_dif = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            y_dif = -self.speed
            y_dif = self.max_till_collision(x_dif, y_dif, opaque_tiles_group)[1]
        elif keys[pygame.K_s]:
            y_dif = self.speed
            y_dif = self.max_till_collision(x_dif, y_dif, opaque_tiles_group)[1]
        if keys[pygame.K_a]:
            self.anim.right = False
            x_dif = -self.speed
            x_dif = self.max_till_collision(x_dif, y_dif, opaque_tiles_group)[0]
        elif keys[pygame.K_d]:
            self.anim.right = True
            x_dif = self.speed
            x_dif = self.max_till_collision(x_dif, y_dif, opaque_tiles_group)[0]
        if not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]):
            self.anim.stand = True
            self.anim.count = 0
            self.image = self.anim.get_anim()
        else:
            self.anim.stand = False
            self.anim.count += 1
            self.anim.count %= (self.anim.n * self.anim.fpu)
            self.image = self.anim.get_anim()
        return x_dif, y_dif

    def moved_sprite(self, x: int, y: int) -> pygame.sprite.Sprite:
        sprite = pygame.sprite.Sprite()
        sprite.rect = self.rect.copy().move(x, y)
        return sprite

    def max_till_collision(self, x_dif, y_dif, opaque_tiles_group):
        moved_sprite = self.moved_sprite(x_dif, y_dif)
        collision = pygame.sprite.spritecollideany(moved_sprite, opaque_tiles_group)
        if collision:
            if x_dif < 0:
                x_dif_till_collision = collision.rect.x + collision.rect.width - moved_sprite.rect.x
            elif x_dif > 0:
                x_dif_till_collision = collision.rect.x - moved_sprite.rect.width - moved_sprite.rect.x
            else:
                x_dif_till_collision = 0

            if y_dif < 0:
                y_dif_till_collision = collision.rect.y + collision.rect.height - moved_sprite.rect.y
            elif y_dif > 0:
                y_dif_till_collision = collision.rect.y - moved_sprite.rect.height - moved_sprite.rect.y
            else:
                y_dif_till_collision = 0

            if abs(x_dif_till_collision) < self.speed:
                x_dif = x_dif_till_collision
            else:
                x_dif = 0
            if abs(y_dif_till_collision) < self.speed:
                y_dif = y_dif_till_collision
            else:
                y_dif = 0
        return x_dif, y_dif


class LavelChanger(Tile):
    def __init__(self,
                 x: int, y: int,
                 texture: pygame.Surface,
                 layer_of_tile_group: pygame.sprite.Group,
                 tile_group: pygame.sprite.Group,
                 transparency: str,
                 size: tuple,
                 player: Player,
                 lavels: Column,
                 direction: typing.Union["d", "u"]) -> None:
        super(LavelChanger, self).__init__(x, y, texture, layer_of_tile_group, tile_group, transparency, size)
        self.player = player
        self.lavels = lavels
        self.direction = direction

    def update(self, x: int, y: int) -> None:
        super(LavelChanger, self).update(x, y)
        if pygame.sprite.collide_rect(self, self.player):
            if self.direction == "d":
                self.lavels.down()
            elif self.direction == "u":
                self.lavels.up()

