import pygame


class Cursor(pygame.sprite.Sprite):
    def __init__(self, image, position, *groups):
        super().__init__(*groups)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=position)

    def update(self):
        mousePosition = pygame.mouse.get_pos()
        self.rect.x = mousePosition[0] - (self.image.get_width() / 2)
        self.rect.y = mousePosition[1] - (self.image.get_height() / 2)
