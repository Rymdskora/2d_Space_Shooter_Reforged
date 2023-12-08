import pygame
from data.shipstatistics import shipStatistics
from scripts.utilities import getPath


class ShipDisplay:
    def __init__(self):
        self.ships = shipStatistics
        self.shipTextures = getPath('images/player/selectableships/', True, True, 6)
        self.shipKeys = self.shipTextures.keys()
        self.shipTitles = getPath('images/userinterface/shiptitles/', True, True, 6)

        self.health = None
        self.armor = None
        self.speed = None
        self.mainWeapon = None
        self.altWeapon = None

        self.selectedShip = 0
        self.currentShip = self.shipTextures['orionsfury']
        self.rotation = 0
        self.animationIndex = 0
        self.animationSpeed = 0.1

    def changeSelectedShip(self, changeTo):
        self.selectedShip += changeTo
        if self.selectedShip >= len(self.shipTextures):
            self.selectedShip = 0
        elif self.selectedShip < 0:
            self.selectedShip = len(self.shipTextures) - 1
        print(self.shipKeys[self.selectedShip])

    def updateStatistics(self, ship):
        try:
            if ship in self.ships.keys():
                newDictionary = self.ships.get(ship)
                for key, value in newDictionary.items():
                    self.__dict__.update({key: value})

        except KeyError:
            print(f'{ship} is not in {self.ships}')

    def animateShip(self):
        self.animationIndex += self.animationSpeed
        self.rotation += 1

        if self.animationIndex >= len(self.currentShip):
            self.animationIndex = 0

        return pygame.transform.rotate(self.currentShip[int(self.animationIndex)], self.rotation)

        # self.screen.blit(self.shipNames[self.selectedShip], (960 - (self.shipNames[self.selectedShip].get_width() / 2), 750))

    def displayShipStatistics(self, screen):
        pass

    def drawSprites(self, screen):
        image = self.animateShip()
        screen.blit(image, ((960 - image.get_height() / 2), (500 - image.get_width() / 2)))
        self.displayShipStatistics(screen)

