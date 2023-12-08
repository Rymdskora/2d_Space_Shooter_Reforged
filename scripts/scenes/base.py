import pygame


class BaseScene:
    def __init__(self, game, screen):
        self.MAINGAME = game
        self.screen = screen
        self.sprites = pygame.sprite.Group()
        self.cursor = self.MAINGAME.mouse
        self.sprites.add(self.cursor)

    def animateBackground(self):
        pass
