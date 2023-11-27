import pygame
import math
from scripts.settings import scale_settings as SSDICT
from scripts.events import EventHandler


class Button:
    def __init__(self, screen, function, position, *attributes):
        self.processAttributes(*attributes)
        self.screen = screen
        self.function = function
        self.scale = SSDICT['UI_SCALE']
        self.scaleBy = (self.textures[0].get_width() * self.scale, self.textures[0].get_height() * self.scale)

        self.image = self.scaleImage(self.textures[0])
        self.rect = self.image.get_rect(center=position)

        self.renderText = self.font.render(self.text, False, self.font_color)
        self.renderTextRect = self.renderText.get_rect(center=self.rect.center)

        # Attributes used for displaying that the button is being hovered over.
        self.imageIndex = 1
        self.imageScrollSpeed = 0.2
        self.alpha = 0
        self.updateAlpha = 5
        self.hoveredImage = self.scaleImage(self.textures[self.imageIndex])
        self.hoveredImageRect = self.hoveredImage.get_rect(center=self.rect.center)

    def scaleImage(self, image):
        return pygame.transform.scale(image, self.scaleBy)

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

    def onMouseHover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.onMouseClick()
            self.onHoverAnimate(True)
        else:
            self.onHoverAnimate(False)

    def onMouseClick(self):
        if EventHandler.checkEventQueue('clicked') is True:
            self.function()

    def onHoverAnimate(self, trueOrFalse):
        self.hoveredImage = self.scaleImage(self.textures[math.floor(self.imageIndex)])
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

    def updateButton(self):
        self.onMouseHover()
        self.drawOnScreen()
