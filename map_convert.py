import pygame
from consts import Tiles_dict, Tile_side, Screen_width, Screen_height
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
               tiles_types_and_groups: dict, player, column):
    startpos_x = (Screen_width - len(layer_map[0]) * Tile_side) // 2
    y_now = (Screen_height - len(layer_map) * Tile_side) // 2
    group_of_this_layer = pygame.sprite.Group()
    for line in layer_map:
        x_now = startpos_x
        for tile in line:
            if tile == "-":
                pass
            elif tile == "d" or "u":
                LavelChanger(x_now, y_now,
                             Tiles_dict[tile]["texture"],
                             group_of_this_layer,
                             tiles_types_and_groups[Tiles_dict[tile]["transparency"]],
                             Tiles_dict[tile]["transparency"],
                             Tiles_dict[tile]["size"],
                             player,
                             column,
                             tile)
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


def init_lavels(player) -> Column:
    lavels = Column()
    for lavel in os.listdir("./maps"):
        layers = []
        tiles_types_and_groups = {"0": pygame.sprite.Group(), "1": pygame.sprite.Group()}
        for layer in os.listdir(os.path.join("./maps", lavel)):
            layer_map = load_layer_as_list(os.path.join("./maps", lavel, layer))
            load_layer(layer_map, layers, tiles_types_and_groups, player, lavels)
        lavels.append(Lavel(layers, tiles_types_and_groups))
    return lavels
