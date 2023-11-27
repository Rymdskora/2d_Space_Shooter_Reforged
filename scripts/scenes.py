import pygame
from scripts.utilities import loadImage, loadFromData, getImageData
from scripts.button import Button
from scripts.entities import PlayerEntity
from scripts.settings import scale_settings as SSDICT


class BaseScene:
    def __init__(self, game, screen):
        self.MAINGAME = game
        self.screen = screen
        self.sprites = pygame.sprite.Group()

    def animateBackground(self):
        pass

class TitleScreen(BaseScene):
    def __init__(self, game, screen):
        super().__init__(game, screen)
        self.font = pygame.font.Font(loadFromData('Ravish Pixelation.ttf'), 36)
        temp_button_dict = {
            'text'      : 'Start',
            'font'      : self.font,
            'textures'  : getImageData('userinterface/', SSDICT['UI_SCALE']),
            'font_color': 'white',
        }
        self.start = Button(self.screen, self.MAINGAME.changeCurrentScene, (960, 540), temp_button_dict)

    def update(self):
        self.screen.fill('black')
        self.start.updateButton()


class GameScreen(BaseScene):
    def __init__(self, game, screen):
        super().__init__(game, screen)
        self.textures = {
            'player'        : getImageData('player/', SSDICT['ENTITY_SCALE']),
            'background'    : getImageData('background/', None)
        }
        self.player = PlayerEntity(self.textures['player'], (64, 540), self.sprites)

    def update(self):
        self.sprites.update()
        self.draw()

    def draw(self):
        self.screen.fill('black')
        self.screen.blit(self.textures['background'][1], (0, 0))
        self.sprites.draw(self.screen)


class EndScreen(BaseScene):
    def __init__(self, game, screen):
        super().__init__(game, screen)

    def update(self):
        pass
