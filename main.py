import pygame
from consts import Screen_size, Player_animlength, Player_left_walk, Player_right_walk, \
    Player_stand, Player_x, Player_y, Player_speed, Player_vision_range
from map_convert import init_lavels
from sprites import Lavel, Player, AnimCount


def draw(screen, lavel: Lavel, player: Player):
    screen.fill(pygame.Color("gray"))
    dif_x, dif_y = player.update(lavel.visible_tiles_types_and_groups["1"])
    lavel.update(dif_x, dif_y)
    lavel.draw(screen)
    screen.blit(player.image, player.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode(Screen_size)
    pygame.display.set_caption("5 НОЧЕЙ С НОСКИНЫМ")
    pygame.display.flip()

    clock = pygame.time.Clock()

    lavels = init_lavels()
    lavel_now = lavels[0]

    player_group = pygame.sprite.Group()
    player_anims = AnimCount(Player_animlength, Player_left_walk, Player_right_walk, Player_stand)
    player = Player(Player_x, Player_y, Player_speed, Player_vision_range, player_anims, player_group)

    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            lavel_now = lavels[0]
        if keys[pygame.K_2]:
            lavel_now = lavels[1]
        if keys[pygame.K_UP]:
            player.speed += 1
        if keys[pygame.K_DOWN]:
            player.speed -= 1

        draw(screen, lavel_now, player)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()