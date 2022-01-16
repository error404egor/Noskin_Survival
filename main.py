import pygame
from consts import Screen_size, Player_animlength, Player_left_walk, Player_right_walk, \
    Player_stand, Player_x, Player_y, Player_speed, Player_vision_range, enemy_x, enemy_y, typical_layer
from map_convert import init_lavels
from sprites import Player, AnimCount, Enemy
from column import Column
T_ONE_X = 0
T_ONE_Y = 0


def draw(screen, lavels: Column, player: Player, enemy: Enemy, level_map_t: list,
         player_cords, speed_x, speed_y):
    screen.fill(pygame.Color("gray"))
    dif_x, dif_y = player.update(lavels.get().visible_tiles_types_and_groups["1"])
    cords = enemy.enemy_find_cords(speed_x, speed_y)
    where_to_go = enemy.find_path_step(level_map_t, player_cords, cords)
    speed_x, speed_y = cords[0] - where_to_go[0], cords[1] - where_to_go[1]
    speed_x, speed_y = speed_x * 5, speed_y * 5
    print(where_to_go, cords, speed_x, speed_y)
    enemy.update(speed_x, speed_y)  # todo
    lavels.get().update(dif_x, dif_y)
    lavels.get().draw(screen)
    screen.blit(player.image, player.rect)
    return speed_x, speed_y


def main():
    global T_ONE_X, T_ONE_Y
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
    dx = len(typical_layer[0]) // 2
    dy = len(typical_layer) // 2
    run = True
    pressed = False

    while run:
        clock.tick(60)
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
        cords_player = lavels.get().player_find_cords(lavels.get().x_stdif,
                                            lavels.get().y_stdif,
                                            lavels.get().standart_x_stdif,
                                            lavels.get().standart_y_stdif, dx, dy)
        cords = draw(screen, lavels, player, enemy, lavels.get().list_layers,
             lavels.get().player_find_cords(lavels.get().x_stdif,
                                            lavels.get().y_stdif,
                                            lavels.get().standart_x_stdif,
                                            lavels.get().standart_y_stdif, dx, dy), T_ONE_X, T_ONE_Y)
        T_ONE_X, T_ONE_Y = cords
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
