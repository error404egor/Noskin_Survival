import typing

from column import Column
import pygame
from consts import Tile_side, Player_x, Player_y, Screen_width, Screen_height, typical_layer, enemy_f_x, enemy_f_y
from boris import rework_map_as_0_1


class Lavel:
    def __init__(self,
                 layers: list[pygame.sprite.Group, ...],
                 visible_tiles_types_and_groups: {"0": pygame.sprite.Group, "1": pygame.sprite.Group},
                 layers_as_list: list[list, ...], enemy):
        self.layers = layers  # слои объектов, которые будут последовательно
        # отрисовываться на карте, каждый слой - группа спрайтов
        self.visible_tiles_types_and_groups = visible_tiles_types_and_groups  # определение группы
        # коллизионных спрайтов и бесколизионных спрайтов (создание двух групп для них).
        self.y_stdif = 0
        self.x_stdif = 0
        self.standart_x_stdif = 0
        self.standart_y_stdif = 0
        self.list_layers = layers_as_list
        self.enemy = enemy

    def update(self,
               dif_x: int, dif_y: int):
        self.x_stdif -= dif_x
        self.y_stdif -= dif_y
        for layer in self.layers:
            layer.update(dif_x, dif_y)  # смещение карты относительно пройденного игроком расстояния
        self.enemy.update(dif_x, dif_y)
        dx = len(typical_layer[0]) // 2
        dy = len(typical_layer) // 2
        player_cords = self.player_find_cords(self.x_stdif, self.y_stdif, self.standart_x_stdif,
                                              self.standart_y_stdif, dx, dy)

    def draw(self,
             screen: pygame.Surface):
        for layer in self.layers:
            layer.draw(screen)  # отрисовка всех слоев карты

    def move_to_spawn(self):
        self.update(self.x_stdif, self.y_stdif)
        self.update(self.standart_x_stdif, self.standart_y_stdif)

    def change_standart_stdif(self, x, y):
        self.standart_x_stdif += x
        self.standart_y_stdif += y
        self.update(self.standart_x_stdif, self.standart_y_stdif)

    def player_find_cords(self, x_stdif, y_stdif, x_standart_stdif, y_standart_stdif, x_f, y_f):
        x_stdif += x_standart_stdif
        y_stdif += y_standart_stdif
        x_f_standart = x_f + (x_standart_stdif // Tile_side)
        y_f_standart = y_f + (y_standart_stdif // Tile_side)
        y_f_sdif = y_f_standart - (y_stdif // Tile_side)
        x_f_stdif = x_f_standart - (x_stdif // Tile_side)
        x_f_stdif, y_f_sdif = y_f_sdif, x_f_stdif
        return y_f_sdif, x_f_stdif


class Tile(pygame.sprite.Sprite):
    def __init__(self,
                 x: int, y: int,  # x, y координаты положения левого верхнего угла тайла
                 texture: pygame.Surface,  # текстура объектика(картиночка.a4)
                 layer_of_tile_group: pygame.sprite.Group,  # объектик прикрепляют к группе слоя(аналогия с ожиданием
                 # попадания в лицей ниу вшэ)
                 tile_group: pygame.sprite.Group,  # объектик прикрепляют к группе колизии(их 2 штуки с колизией и без)
                 # (аналогия с хайпиками авангарда и с нехайпиками неавангарда)
                 transparency: str,  # 0 для бесколлизионных, 1 для коллизионных
                 size: tuple) -> None:  # размер тайла width, height
        super().__init__()
        self.image = texture  # загрузка картинки спрайта
        self.rect = pygame.rect.Rect(x + (Tile_side - size[0]) // 2, y + (Tile_side - size[1]) // 2, *size)  # создание
        # тела тайла и размещение по его центру
        self.transparency = transparency  # база
        self.add(layer_of_tile_group, tile_group)  # добавка в группу слоя и тп смотри в небеса

    def update(self, x: int, y: int) -> None:
        self.rect.x -= x  # смещение верхней точки левой (ox) тайла на -x при движении додика вправо, иначе x
        self.rect.y -= y  # то же самое но уже oy и y


class AnimCount:  # забейте тут всякий бред
    def __init__(self, n: int, left_anims: list, right_anims: list, stand_anim: str,
                 count=0, fpu=1, right=True, stand=True) -> None:
        self.n = n  # количество картинок анимации
        self.count = count % (n * fpu)  # картинка в текущий момент
        self.right = right  # флаг ходьбы вправо
        self.stand = stand  # флаг стояния
        self.fpu = fpu  # скорость смены картинки в условных единицах
        self.left_anims = left_anims  # анимация левой ходьбы
        self.right_anims = right_anims  # анимация правой ходьбы
        self.stand_anim = stand_anim  # анимация стояния (1 картинка)

    def get_anim(self) -> pygame.Surface:
        if self.stand:
            return self.stand_anim  # при стоянии возвращает список анимаций стояния и так далее
        elif self.right:
            return self.right_anims[int(self.count // self.fpu)]
        else:
            return self.left_anims[int(self.count // self.fpu)]


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int, vision_range: int,
                 anim: AnimCount, player_group: pygame.sprite.Group) -> None:
        super().__init__()
        self.anim = anim  # объект анимации для игрока
        self.image = self.anim.get_anim()  # запихивание самой первой картинки амогуса в ег self image
        self.rect = self.image.get_rect(center=(x, y))  # создание границ амогусика
        self.speed = speed  # скорость амогуса пиксель/кадр
        self.vision_range = vision_range  # todo in fact
        player_group.add(self)  # добавка в группу спрайтов игрока

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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int, vision_range: int,
                 anim: AnimCount, player_group: pygame.sprite.Group) -> None:
        super().__init__()
        self.x = enemy_f_x * Tile_side
        self.y = enemy_f_y * Tile_side
        self.anim = anim  # объект анимации для врага
        self.image = self.anim.get_anim()  # запихивание самой первой картинки амогуса в ег self image
        self.rect = self.image.get_rect()  # создание границ врага
        width = len(typical_layer[0])
        height = len(typical_layer)
        self.rect.x = self.x - (width - Screen_width) // 2
        self.rect.y = self.y - (height - Screen_height) // 2
        print(self.rect)
        self.speed = speed  # скорость врага пиксель/кадр
        self.vision_range = vision_range  # todo in fact
        player_group.add(self)  # добавка в группу спрайтов врага

    def update(self, x: int, y: int) -> None:
        self.rect.x -= x
        self.rect.y -= y

    def find_path_step(self, level: str, start, target):
        INF = 1000
        start, target = target, start
        x, y = start
        map_ = rework_map_as_0_1(level)
        # for elem in map_:
        #    print(elem)
        # print('\n')
        # print('\n')
        width = len(map_[0])
        height = len(map_)
        distance = [[INF] * width for _ in range(height)]
        distance[y][x] = 0
        prev = [[None] * width for _ in range(height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < width and 0 <= next_y < height\
                        and map_[next_y][next_x] is 0 and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        # for elem in distance:
        #    print(elem)
        # print('\n')
        # print('\n')
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y

    def enemy_find_cords(self, dx=0, dy=0):
        self.x -= dx
        self.y -= dy
        return self.x // Tile_side, self.y // Tile_side


class LavelChanger(Tile):
    def __init__(self,
                 x: int, y: int,
                 texture: pygame.Surface,
                 layer_of_tile_group: pygame.sprite.Group,
                 tile_group: pygame.sprite.Group,
                 transparency: str,
                 size: tuple,
                 player: Player,
                 enemy: Enemy,
                 lavels: Column,
                 direction: typing.Union["d", "u"]) -> None:
        super(LavelChanger, self).__init__(x, y, texture, layer_of_tile_group, tile_group, transparency, size)
        self.player = player
        self.enemy = enemy
        self.lavels = lavels
        self.direction = direction

    def update(self, x: int, y: int) -> None:
        super(LavelChanger, self).update(x, y)
        if pygame.sprite.collide_rect(self, self.player):
            if self.direction == "d":
                self.lavels.get().move_to_spawn()
                self.lavels.down()
            elif self.direction == "u":
                self.lavels.get().move_to_spawn()
                self.lavels.up()