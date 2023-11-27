import pygame
import math
from scripts.settings import game_settings as GSDICT


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, identifier,  images, position, *groups):
        super().__init__(*groups)
        self.entityType = identifier
        self.textures = images
        self.image = self.textures['idle'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(midleft=position)
        self.direction = [0, 0]
        self.speed = 0

        self.animated = None
        self.imageIndex = 0
        self.animationSpeed = 0.25

    def moveEntity(self):
        self.rect.y += self.direction[1] * self.speed

    def animateEntity(self):
        self.image = self.textures[self.animated][math.floor(self.imageIndex)]
        self.imageIndex += self.animationSpeed
        if self.imageIndex >= len(self.textures['idle']):
            self.imageIndex = 0

    def clampPosition(self):
        if self.rect.y <= 0:
            self.rect.midtop = (self.rect.midtop[0], 0)
        if self.rect.midbottom[1] >= GSDICT['SCREEN_HEIGHT']:
            self.rect.midbottom = (self.rect.midbottom[0], GSDICT['SCREEN_HEIGHT'])


class PlayerEntity(PhysicsEntity):
    def __init__(self, identifier, image, position, *groups):
        super().__init__(identifier, image, position, *groups)
        self.currentSpeed = 3

    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.direction[1] = -1
            self.animated = 'up'
        elif keys[pygame.K_LSHIFT]:
            self.direction[1] = 1
            self.animated = 'down'
        else:
            self.direction[1] = 0
            self.animated = 'idle'

    def moveEntity(self):
        self.rect.y += self.direction[1] * self.currentSpeed

    def update(self):
        self.getInput()
        self.moveEntity()
        self.clampPosition()
        self.animateEntity()


# TODO - Think about how this should properly work,
#  we somehow need to pass textures to this class upon instantiation. If we don't do this,
#  then we'll end up loading the same image EVERY time an object is created.
class ProjectileEntity(PhysicsEntity):
    def __init__(self, direction, identifier, image, position, *groups):
        super().__init__(identifier, image, position, *groups)
        self.direction = [direction, 0]
        self.speed = 7

    def update(self):
        self.moveEntity()
