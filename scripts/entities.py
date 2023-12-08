import pygame
import math
from scripts.settings import game_settings as GSDICT


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, identifier, images, position, *groups):
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
        self.rect.x += self.direction[0] * self.speed
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

    def killEntity(self):
        self.kill()


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


class ProjectileEntity(PhysicsEntity):
    def __init__(self, direction, identifier, images, position, *groups):
        super().__init__(identifier, images, position, *groups)
        self.direction = [direction, 0]
        self.speed = 7
        self.animated = 'right'

    def clampPosition(self):
        if self.rect.x + self.image.get_width() > GSDICT['SCREEN_WIDTH']:
            self.killEntity()
        if self.rect.x + self.image.get_width() < 0:
            self.killEntity()

    def animateEntity(self):
        self.image = self.textures[self.animated][math.floor(self.imageIndex)]
        self.imageIndex += self.animationSpeed
        if self.imageIndex >= len(self.textures['right']):
            self.imageIndex = 0

    def update(self):
        self.moveEntity()
        self.clampPosition()
        self.animateEntity()
