import pygame
from consts import Screen_height, Screen_size


class Bar:
    def __init__(self, text="ключей: ", text2="Все ключи собраны! Иди к двери и нажми E!"):
        self.text = text
        self.text2 = text2
        self.count = 0
        self.n = 0
        self.font = pygame.font.Font(None, 50)
        self.t = None
        self.update_t()
        self.done = False

    def add_to_n(self, n=1):
        self.n += n
        self.update_t()

    def add_to_count(self, c=1):
        self.count += c
        self.update_t()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.t, (20, 50))
        if self.n <= self.count:
            screen.blit(self.font.render(self.text2, True, (255, 255, 255)), (20, Screen_height - 50))

    def update_t(self):
        self.t = self.font.render(self.text + str(self.count) + "/" + str(self.n), True, (255, 255, 255))


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def pause(screen):
    screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0,))
    greenButton = Button((0, 255, 0), 280, 255, 300, 100, "Продолжить")
    redButton = Button((255, 0, 0), 280, 380, 300, 100, "Меню")
    run = True
    while run:
        screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0,))
        greenButton.draw(screen, (0, 0, 0))
        redButton.draw(screen, (0, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if greenButton.isOver(pos):
                    return None
                if redButton.isOver(pos):
                    run = False
                    return run

            if event.type == pygame.MOUSEMOTION:
                if greenButton.isOver(pos):
                    greenButton.color = (105, 105, 105)
                else:
                    greenButton.color = (0, 255, 0)
                if redButton.isOver(pos):
                    redButton.color = (105, 105, 105)
                else:
                    redButton.color = (255, 0, 0)


def menu(screen: pygame.Surface, game):
    screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0, ))
    greenButton = Button((0, 255, 0), 280, 255, 250, 100, "Start")
    redButton = Button((255, 0, 0), 280, 380, 250, 100, "Quit")
    run = True
    while run:
        screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0, ))
        greenButton.draw(screen, (0, 0, 0))
        redButton.draw(screen, (0, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if greenButton.isOver(pos):
                    game(screen)
                if redButton.isOver(pos):
                    run = False
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if greenButton.isOver(pos):
                    greenButton.color = (105, 105, 105)
                else:
                    greenButton.color = (0, 255, 0)
                if redButton.isOver(pos):
                    redButton.color = (105, 105, 105)
                else:
                    redButton.color = (255, 0, 0)
