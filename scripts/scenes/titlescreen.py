import pygame
from scripts.scenes.base import BaseScene
from scripts.utilities import getPath
from scripts.settings import scale_settings as SSDICT
from scripts.button import Button
from functools import partial
from scripts.displayshipdetails import ShipDisplay

class TitleScreen(BaseScene):
    def __init__(self, game, screen):
        super().__init__(game, screen)
        self.displayShip = ShipDisplay()
        self.textures = {
            'start'     :   getPath('images/userinterface/button/', True, True, SSDICT['UI_SCALE']),
            'nextR'     :   getPath('images/userinterface/nextbuttonR/', True, True, SSDICT['UI_SCALE']),
            'nextL'     :   getPath('images/userinterface/nextbuttonL/', True, True, SSDICT['UI_SCALE']),
            'titlelogo' :   getPath('images/ts_logo.png', True, True, 8),
            'background':   getPath('images/background/titlebackground', True, False, None)
        }
        self.buttons = {
            'startButton'   :   {
                'text'      : 'Start',
                'font'      : self.MAINGAME.font,
                'textures'  : self.textures['start'],
                'font_color': 'white',
            },
            'nextButtonR'    :   {
                'text'      : '',
                'font'      : self.MAINGAME.font,
                'textures'  : self.textures['nextR'],
                'font_color': 'white',
            },
            'nextButtonL': {
                'text': '',
                'font': self.MAINGAME.font,
                'textures': self.textures['nextL'],
                'font_color': 'white',
            }
        }
        self.start = Button(self.screen, self.MAINGAME.changeCurrentScene, (960, 900), self.buttons['startButton'])
        self.nextR = Button(self.screen, partial(self.displayShip.changeSelectedShip, 1), (1200, 900), self.buttons['nextButtonR'])
        self.nextL = Button(self.screen, partial(self.displayShip.changeSelectedShip, -1), (720, 900), self.buttons['nextButtonL'])

        # Reserved for animating the background.
        self.scrollBackground = 0

    def animateBackground(self):
        for y in range(0, (len(self.textures['background']) + 1)):
            speed = 1
            for image in self.textures['background']:
                self.screen.blit(image, (0, (y * -1080) + (self.scrollBackground * speed)))
                speed += 1
        self.scrollBackground += 1
        if self.scrollBackground >= 1080:
            self.scrollBackground = 0

    def update(self):
        self.screen.fill('black')
        self.animateBackground()
        self.sprites.update()
        self.start.updateButton(self.cursor)
        self.nextR.updateButton(self.cursor)
        self.nextL.updateButton(self.cursor)
        self.draw()

    def draw(self):
        self.displayShip.drawSprites(self.screen)
        self.screen.blit(self.textures['titlelogo'], (960 - self.textures['titlelogo'].get_width() / 2, 100))
        self.sprites.draw(self.screen)
