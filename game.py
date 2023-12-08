import pygame
import sys
from scripts.events import EventHandler
from scripts.settings import game_settings as GSDICT
from scripts.scenes.titlescreen import TitleScreen
from scripts.utilities import getPath
from scripts.cursor import Cursor
import math

class MainGame:
    def __init__(self):
        pygame.init()
        self.flags = pygame.SCALED
        self.screen = pygame.display.set_mode((GSDICT['SCREEN_WIDTH'], GSDICT['SCREEN_HEIGHT']), self.flags, vsync=0)
        self.font = pygame.font.Font(getPath('Ravish Pixelation.ttf', False, False, None), 36)
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.mouse.set_visible(False)
        self.textures = {
            'cursor'    : getPath('images/cursor.png', True, True, 5)
        }
        self.mouse = Cursor(self.textures['cursor'], pygame.mouse.get_pos())
        self.sceneList = {
            'title' : TitleScreen,
            'game'  : None,
            'end'   : None,
        }
        self.currentScene = self.sceneList['title'](self, self.screen)

    def mainLoop(self):
        while self.running:
            self.handleEvents()
            self.currentScene.update()

            self.screen.blit(self.font.render(f'{math.floor(self.clock.get_fps())}', False, 'white'), (0, 0))

            pygame.display.flip()
            self.clock.tick(GSDICT['FPS'])

    def handleEvents(self):
        EventHandler.events = pygame.event.get()
        if EventHandler.checkEventQueue('quit') is True:
            self.quitGame()

    def changeCurrentScene(self):
        self.currentScene = self.sceneList['game'](self, self.screen)

    @staticmethod
    def quitGame():
        pygame.quit()
        sys.exit()


game = MainGame()
game.mainLoop()
