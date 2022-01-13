import pygame


class Bar:
    def __init__(self, text="ключей: "):
        self.text = text
        self.count = 0
        self.n = 0
        self.font = pygame.font.Font(None, 50)
        self.t = None
        self.update_t()

    def add_to_n(self, n):
        self.n += n
        self.update_t()

    def add_to_count(self, c=1):
        self.count += c
        self.update_t()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.t, (20, 50))

    def update_t(self):
        self.t = self.font.render(self.text + str(self.count) + "/" + str(self.n), True, (255, 255, 255))