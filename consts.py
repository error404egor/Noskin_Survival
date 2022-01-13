import os
import pygame
import csv


Screen_width = 1000
Screen_height = 700
Screen_size = (Screen_width, Screen_height)

Player_width = 96
Player_height = 96
Player_x = Screen_width // 2
Player_y = Screen_height // 2
Player_speed = 10
Player_fpu = 1
Player_vision_range = 300
Player_side = 90
Player_right_walk = [pygame.transform.scale(pygame.image.load(os.path.join("./textures/Walk Right", i)),
                     (Player_side, Player_side, )) for i in os.listdir("./textures/Walk Right")]
Player_left_walk = [pygame.transform.scale(pygame.image.load(os.path.join("./textures/Walk Left", i)),
                    (Player_side, Player_side, )) for i in os.listdir("./textures/Walk Left")]
Player_animlength = len(Player_right_walk)
Player_stand = pygame.transform.scale(pygame.image.load("./textures/idle.png"), (Player_side, Player_side, ))

with open("tiles.csv", "r") as tiles:
    Tiles_list = list(csv.DictReader(tiles))
    Tiles_dict = {elem["char"]: {"transparency": elem["transparency"],
                                 "texture": pygame.transform.scale(pygame.image.load(elem["texture"]),
                                                                   (int(elem["width"]), int(elem["height"]))),
                                 "size": (int(elem["width"]),
                                          int(elem["height"]))} for elem in Tiles_list}
Tile_side = Tiles_dict[" "]["size"][0]
KeyChar = "k"
Number_of_keys_at_floor = 1

Level0 = "map.txt"
