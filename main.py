import pygame
from consts import Screen_size, Player_animlength, Player_left_walk, Player_right_walk, \
    Player_stand, Player_x, Player_y, Player_speed, Player_vision_range
from map_convert import init_lavels
from sprites import Player, AnimCount
from column import Column
from menuBar import Bar, pause, menu, lose, win
#  picking keys


def draw(screen, lavels: Column, player: Player, bar: Bar):
    screen.fill(pygame.Color("black"))
    dif_x, dif_y = player.update(lavels.get().visible_tiles_types_and_groups["1"])
    lavels.get().update(dif_x, dif_y)
    lavels.get().draw(screen)
    pygame.draw.circle(screen, pygame.Color("black"), player.rect.center,
                       Screen_size[0], width=Screen_size[0] - player.vision_range)
    bar.draw(screen)
    screen.blit(player.image, player.rect)


def game(screen):
    bar = Bar()

    clock = pygame.time.Clock()

    player_group = pygame.sprite.Group()
    player_anims = AnimCount(Player_animlength, Player_left_walk, Player_right_walk, Player_stand)
    player = Player(Player_x, Player_y, Player_speed, Player_vision_range, player_anims, player_group)

    lavels = init_lavels(player, bar)

    run = True
    pressed = False

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
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
        elif keys[pygame.K_ESCAPE]:
            if pause(screen) == False:
                return 0
        else:
            pressed = False

        draw(screen, lavels, player, bar)
        pygame.display.flip()
        if bar.done:
            win(screen)
            run = False


def main():
    pygame.init()
    screen = pygame.display.set_mode(Screen_size)
    pygame.display.set_caption("5 НОЧЕЙ С НОСКИНЫМ")
    pygame.display.flip()
    menu(screen, game)


if __name__ == "__main__":
    main()
