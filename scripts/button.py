import pygame
import math
from scripts.events import EventHandler


class Button:
    def __init__(self, screen, function, position, *attributes):
        self.processAttributes(*attributes)
        self.screen = screen
        self.function = function

        self.image = self.textures[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=position)

        self.renderText = self.font.render(self.text, False, self.font_color)
        self.renderTextRect = self.renderText.get_rect(center=self.rect.center)

        # Attributes used for displaying that the button is being hovered over.
        self.imageIndex = 1
        self.imageScrollSpeed = 0.2
        self.alpha = 0
        self.updateAlpha = 5
        self.hoveredImage = self.textures[self.imageIndex]
        self.hoveredImageRect = self.hoveredImage.get_rect(center=self.rect.center)

    def processAttributes(self, attributes):
        buttonSettings = {
            'text'          : None,
            'font'          : None,
            # Textures FIRST IMAGE should be the base or non-hovered image!
            # WHY? We loop over the extra textures to display the hovered animation.
            # If we didn't do this we'd have to devise some stupid skip x image mechanism.
            'textures'      : None,
            'font_color'    : None,
        }
        for argument in attributes:
            buttonSettings[argument] = attributes[argument]
        self.__dict__.update(buttonSettings)

    def onMouseHover(self, cursor):
        if self.mask.overlap(cursor.mask, (cursor.rect[0] - self.rect[0], cursor.rect[1] - self.rect[1])):
            self.onMouseClick()
            self.onHoverAnimate(True)
        else:
            self.onHoverAnimate(False)

    def onMouseClick(self):
        if EventHandler.checkEventQueue('clicked') is True:
            try:
                self.function()
            except TypeError:
                print(f'Button {self} has no function.')

    def onHoverAnimate(self, trueOrFalse):
        self.hoveredImage = (self.textures[math.floor(self.imageIndex)])
        self.hoveredImage.set_alpha(self.alpha)
        self.imageIndex += self.imageScrollSpeed
        if self.imageIndex >= len(self.textures):
            self.imageIndex = 1

        if trueOrFalse is True:
            self.alpha += self.updateAlpha
        elif trueOrFalse is False:
            self.alpha -= self.updateAlpha

        self.alpha = min(255, max(0, self.alpha))

    def drawOnScreen(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.hoveredImage, self.hoveredImageRect)
        self.screen.blit(self.renderText, self.renderTextRect)

    def updateButton(self, cursor):
        self.onMouseHover(cursor)
        self.drawOnScreen()
