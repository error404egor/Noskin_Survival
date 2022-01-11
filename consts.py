import os
import pygame
import csv


Screen_width = 1000
Screen_height = 700
Screen_size = (Screen_width, Screen_height)

#  Player_width = 96   todo cut down
#  Player_height = 96   todo cut down
Player_x = Screen_width // 2  # место спавна игрока (x)
Player_y = Screen_height // 2  # место спавна игрока (y)
Player_speed = 5  # скорость игрока за кадр/пиксель
#  Player_fpu = 1   todo cut down
Player_vision_range = 300  # радиус круга вокруг игрока
Player_side = 85  # сторона игрока при его движении
Player_right_walk = [pygame.transform.scale(pygame.image.load(os.path.join("./textures/Walk Right", i)),
                     (Player_side, Player_side, )) for i in os.listdir("./textures/Walk Right")]  # список картинок
# анимации объектов, трансормированный по длине player_side для анимации правого бега
Player_left_walk = [pygame.transform.scale(pygame.image.load(os.path.join("./textures/Walk Left", i)),
                    (Player_side, Player_side, )) for i in os.listdir("./textures/Walk Left")]  # список картинок
# анимации объектов, трансормированный по длине player_side для анимации левого бега
Player_animlength = len(Player_right_walk)  # длина анимации (количество картинок анимации)
Player_stand = pygame.transform.scale(pygame.image.load("./textures/idle.png"), (Player_side, Player_side, ))  #картин
# ка стоящего амонгуса

with open("tiles.csv", "r") as tiles:
    Tiles_list = list(csv.DictReader(tiles))
    Tiles_dict = {elem["char"]: {"transparency": elem["transparency"],
                                 "texture": pygame.transform.scale(pygame.image.load(elem["texture"]),
                                                                   (int(elem["width"]), int(elem["height"]))),
                                 "size": (int(elem["width"]),
                                          int(elem["height"]))} for elem in Tiles_list}

# из таблицы tiles.csv создан пригодный для программы словарь

Tile_side = Tiles_dict[" "]["size"][0]  # размеры тайла(эталонные)

#  Level0 = "map.txt" todo to cut down one more shit
