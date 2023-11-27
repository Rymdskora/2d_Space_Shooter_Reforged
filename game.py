import pygame
import sys
from scripts.events import EventHandler
from scripts.settings import game_settings as GSDICT
from scripts.scenes import TitleScreen, GameScreen, EndScreen
from scripts.utilities import loadFromData
import math

class MainGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GSDICT['SCREEN_WIDTH'], GSDICT['SCREEN_HEIGHT']), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.sceneList = {
            'title' : TitleScreen,
            'game'  : GameScreen,
            'end'   : EndScreen,
        }
        self.currentScene = self.sceneList['title'](self, self.screen)
        self.font = pygame.font.Font(loadFromData('Ravish Pixelation.ttf'), 36)

    def mainLoop(self):
        while self.running:
            self.handleEvents()
            self.currentScene.update()

            self.screen.blit(self.font.render(f'{math.floor(self.clock.get_fps())}', False, 'white'), (0, 0))

            pygame.display.update()
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
