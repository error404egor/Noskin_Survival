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


class Text:
    def __init__(self, color, x, y, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render(self.text, 1, self.color)
        screen.blit(text, (self.x, self.y, ))


def pause(screen):
    screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0,))
    green_button = Button((0, 255, 0), 280, 255, 300, 100, "Продолжить")
    red_button = Button((255, 0, 0), 280, 380, 300, 100, "Меню")
    run = True
    while run:
        screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0,))
        green_button.draw(screen, (0, 0, 0))
        red_button.draw(screen, (0, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if green_button.isOver(pos):
                    return None
                if red_button.isOver(pos):
                    run = False
                    return run

            if event.type == pygame.MOUSEMOTION:
                if green_button.isOver(pos):
                    green_button.color = (105, 105, 105)
                else:
                    green_button.color = (0, 255, 0)
                if red_button.isOver(pos):
                    red_button.color = (105, 105, 105)
                else:
                    red_button.color = (255, 0, 0)


def menu(screen: pygame.Surface, game):
    screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0, ))
    green_button = Button((0, 255, 0), 280, 255, 250, 100, "Start")
    red_button = Button((255, 0, 0), 280, 380, 250, 100, "Quit")
    run = True
    while run:
        screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0, ))
        green_button.draw(screen, (0, 0, 0))
        red_button.draw(screen, (0, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if green_button.isOver(pos):
                    game(screen)
                if red_button.isOver(pos):
                    run = False
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if green_button.isOver(pos):
                    green_button.color = (105, 105, 105)
                else:
                    green_button.color = (0, 255, 0)
                if red_button.isOver(pos):
                    red_button.color = (105, 105, 105)
                else:
                    red_button.color = (255, 0, 0)


def over(screen: pygame.Surface, text):
    screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0, ))
    green_button = Button((0, 255, 0), 280, 300, 250, 100, "Продолжить")
    text = Text((255, 255, 255), 280, 255, text)
    run = True
    while run:
        screen.blit(pygame.transform.scale(pygame.image.load("./textures/menu_screen.jpg"), Screen_size), (0, 0, ))
        green_button.draw(screen, (0, 0, 0))
        text.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if green_button.isOver(pos):
                    return 0

            if event.type == pygame.MOUSEMOTION:
                if green_button.isOver(pos):
                    green_button.color = (105, 105, 105)
                else:
                    green_button.color = (0, 255, 0)


def win(screen):
    return over(screen, "Вы сбежали от Бориса!")


def lose(screen):
    return over(screen, "Вы стали кормом Бориса.")