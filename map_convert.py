import pygame
from consts import Tiles_dict, Tile_side, Screen_width, Screen_height, Player_x, Player_y
from sprites import Tile, Lavel, LavelChanger
import os
from column import Column


def load_layer_as_list(file: str) -> list:
    with open(file, "r") as map_:
        level_map = []
        for line in map_:
            line = line.strip()
            level_map.append(line)
        return level_map


def load_layer(layer_map: list,
               layers: list,
               tiles_types_and_groups: dict, player, enemy, column):
    startpos_x = (Screen_width - (len(layer_map[0]) * Tile_side)) // 2
    y_now = (Screen_height - (len(layer_map) * Tile_side)) // 2
    group_of_this_layer = pygame.sprite.Group()  # ?
    standart_y_stdif = 0
    standart_x_stdif = 0
    for line in layer_map:
        x_now = startpos_x
        for tile in line:
            if tile == "-":
                pass
            elif tile == "d" or tile == "u":
                LavelChanger(x_now, y_now,
                             Tiles_dict[tile]["texture"],
                             group_of_this_layer,
                             tiles_types_and_groups[Tiles_dict[tile]["transparency"]],
                             Tiles_dict[tile]["transparency"],
                             Tiles_dict[tile]["size"],
                             player,
                             enemy,
                             column,
                             tile)
            elif tile == "s":
                standart_x_stdif = (x_now + (Tile_side // 2)) - Player_x
                standart_y_stdif = (y_now + (Tile_side // 2)) - Player_y
                Tile(x_now, y_now,
                     Tiles_dict[tile]["texture"],
                     group_of_this_layer,
                     tiles_types_and_groups[Tiles_dict[tile]["transparency"]],
                     Tiles_dict[tile]["transparency"],
                     Tiles_dict[tile]["size"])
            else:
                Tile(x_now, y_now,
                     Tiles_dict[tile]["texture"],
                     group_of_this_layer,
                     tiles_types_and_groups[Tiles_dict[tile]["transparency"]],
                     Tiles_dict[tile]["transparency"],
                     Tiles_dict[tile]["size"])
            x_now += Tile_side
        y_now += Tile_side
    layers.append(group_of_this_layer)
    return standart_x_stdif, standart_y_stdif


def init_lavels(player, enemy) -> Column:
    lavels = Column()
    lavel_as_list = []
    for lavel in os.listdir("./maps"):
        standart_x_stdif, standart_y_stdif = 0, 0
        layers = []
        layer_as_list = []
        tiles_types_and_groups = {"0": pygame.sprite.Group(), "1": pygame.sprite.Group()}  # ?
        for layer in os.listdir(os.path.join("./maps", lavel)):
            layer_map = load_layer_as_list(os.path.join("./maps", lavel, layer))
            layer_as_list.append(layer_map)
            if not(standart_x_stdif or standart_y_stdif):
                standart_x_stdif, standart_y_stdif = load_layer(layer_map, layers,
                                                                tiles_types_and_groups, player, enemy, lavels)
            else:
                load_layer(layer_map, layers, tiles_types_and_groups, player, enemy, lavels)
        lavel_as_list.append(layer_as_list)
        newlavel = Lavel(layers, tiles_types_and_groups, lavel_as_list, enemy)
        newlavel.change_standart_stdif(standart_x_stdif, standart_y_stdif)
        lavels.append(newlavel)

    return lavels
