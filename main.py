import pygame
from consts import Screen_size, Player_animlength, Player_left_walk, Player_right_walk, \
    Player_stand, Player_x, Player_y, Player_speed, Player_vision_range, enemy_x, enemy_y, typical_layer, Tile_side, \
    enemy_speed, enemy_f_x, enemy_f_y
from map_convert import init_lavels
from sprites import Player, AnimCount, Enemy
from column import Column
from math import ceil
T_ONE_X, T_ONE_Y = 0, 0
GO_OR_FIND_WAY, AMOUNT_OF_STEPS, STEPS, ENEMY_CORDS = True, ceil(Tile_side / enemy_speed), 0, (enemy_f_x, enemy_f_y)


def draw(screen, lavels: Column, player: Player, enemy: Enemy):
    screen.fill(pygame.Color("gray"))
    dif_x, dif_y = player.update(lavels.get().visible_tiles_types_and_groups["1"])
    lavels.get().update(dif_x, dif_y)
    lavels.get().draw(screen)
    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)


def main():
    global T_ONE_X, T_ONE_Y, GO_OR_FIND_WAY, AMOUNT_OF_STEPS, STEPS, ENEMY_CORDS
    pygame.init()
    screen = pygame.display.set_mode(Screen_size)
    pygame.display.set_caption("5 НОЧЕЙ С НОСКИНЫМ")
    pygame.display.flip()

    clock = pygame.time.Clock()

    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    player_anims = AnimCount(Player_animlength, Player_left_walk, Player_right_walk, Player_stand)
    player = Player(Player_x, Player_y, Player_speed, Player_vision_range, player_anims, player_group)

    enemy = Enemy(enemy_x, enemy_y, Player_speed, Player_vision_range, player_anims, enemy_group)
    lavels = init_lavels(player, enemy)
    dx = len(typical_layer[0]) / 2
    dy = len(typical_layer) / 2  # нюхвй бебру
    run = True
    pressed = False

    while run:
        clock.tick(60)  # ok
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            if not pressed:
                lavels.down()
                pressed = True
        elif keys[pygame.K_2]:
            if not pressed:
                lavels.up()
                pressed = True
        elif keys[pygame.K_UP]:
            if not pressed:
                player.speed += 1
                pressed = True
        elif keys[pygame.K_DOWN]:
            if not pressed:
                player.speed -= 1
                pressed = True
        else:
            pressed = False

        draw(screen, lavels, player, enemy)
        if GO_OR_FIND_WAY:
            cords = enemy.where_to_move(lavels.get().list_layers,
             lavels.get().player_find_cords(lavels.get().x_stdif,
                                            lavels.get().y_stdif,
                                            lavels.get().standart_x_stdif,
                                            lavels.get().standart_y_stdif, dx, dy), ENEMY_CORDS,
                                        T_ONE_X // enemy_speed, T_ONE_Y // enemy_speed)
            print(cords)
            ENEMY_CORDS = cords[2][0], cords[2][1]
            GO_OR_FIND_WAY = False
            T_ONE_X, T_ONE_Y = cords[0], cords[1]
        else:
            if STEPS != AMOUNT_OF_STEPS:
                enemy.move_enemy(T_ONE_X, T_ONE_Y)
                STEPS += 1
            else:
                GO_OR_FIND_WAY = True
                STEPS = 0
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
