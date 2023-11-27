import pygame
import math

# Suggested input for a button!
# btn_settings = {
#     'text' : 'start',
#     'font' : pygame.font.Font(GlobalSettings.pixeltype, 48),
#     'font_color' : 'white',
#     'hover_images' : images
# }
# TODO, KILL THIS CLASS (WHEN I FEEL LIKE IT).

class Button:
    def __init__(self, image, position, command, **kwargs):
        self.process_kwargs(kwargs)
        self.image = pygame.transform.scale(image, ((image.get_width() * Setting.UI_SCALE), (image.get_height() * Setting.UI_SCALE))).convert()
        self.rect = self.image.get_rect(center=position)
        self.function = command
        self.text = self.font.render(self.text, False, self.font_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

        # USED FOR HOVERED SHIT
        self.hovered_rect = self.hover_images[1].get_rect(topleft=self.rect.topleft)
        self.scroll_images = 1
        self.current_alpha = 0
        self.SCROLL_SPEED = 0.01
        self.CHANGE_ALPHA = 0.25

    def process_kwargs(self, kwargs):
        settings = {
            'text'          : None,
            'font'          : None,
            'font_color'    : None,
            'hover_images'   : None,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                print("SOMETHING'S WRONG, I CAN FEEL IT! (BUTTON)")
        self.__dict__.update(settings)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.function()

    def is_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.current_alpha >= 0:
            current_image = self.hover_images[math.floor(self.scroll_images)]
            current_image.set_alpha(self.current_alpha)

            if self.is_hovered():
                self.update_and_blit(surface, current_image)
                if self.current_alpha < 255:
                    self.current_alpha += self.CHANGE_ALPHA
            else:
                self.update_and_blit(surface, current_image)
                if self.current_alpha > 0:
                    self.current_alpha -= self.CHANGE_ALPHA

        surface.blit(self.text, self.text_rect)

    def update_and_blit(self, surface, current_image):
        if self.scroll_images <= 15:
            surface.blit(pygame.transform.scale(current_image,
            ((current_image.get_width() * Setting.UI_SCALE), (current_image.get_height() * Setting.UI_SCALE))).convert_alpha(), self.hovered_rect)
        self.scroll_images += self.SCROLL_SPEED
        if self.scroll_images > 15:
            self.scroll_images = 1
