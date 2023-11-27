import pygame
import math
from scripts.settings import scale_settings as SSDICT


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, images, position, *groups):
        super().__init__(*groups)
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


class PlayerEntity(PhysicsEntity):
    def __init__(self, image, position, *groups):
        super().__init__(image, position, *groups)
        self.currentSpeed = 3
        self.maxSpeed = 3

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
        self.animateEntity()
